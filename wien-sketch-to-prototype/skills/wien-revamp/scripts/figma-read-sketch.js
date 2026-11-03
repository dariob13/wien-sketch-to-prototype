// Read-only use_figma script: turns a rough Figma sketch into a compact outline.
// Replace __NODE_ID__ with the node id from the link (1-2 → "1:2"). The node can be
// a page, a section, or one frame. A single frame pulls in the frames its prototype
// links point to (up to MAX_PAGES).
//
// Output: { pages: [ { id, name, w, h, fill, tree, links } ], arrows, notes }
// Every box in `tree` has bounds relative to its page frame, and its children are
// nested by GEOMETRY (smallest box that contains it), not by layer hierarchy,
// because sketchers often draw text on top of rectangles as siblings.
// The script does not change the file.

const TARGET_ID = "__NODE_ID__";
const MAX_PAGES = 12;
const TOL = 2;

const root = await figma.getNodeByIdAsync(TARGET_ID);
if (!root) return { error: "Node not found: " + TARGET_ID };
let pg = root;
while (pg && pg.type !== "PAGE") pg = pg.parent;
if (pg && pg.id !== figma.currentPage.id) await figma.setCurrentPageAsync(pg);

const DEFAULT_NAME = /^(Rectangle|Frame|Group|Ellipse|Line|Vector|Polygon|Star|Text|Union|Subtract|Intersect|Exclude|Image|Section|Component|Instance|Auto ?layout|Container|Slice|Arrow)( \d+)?$/i;
const BOXY = new Set(["FRAME", "RECTANGLE", "GROUP", "INSTANCE", "COMPONENT", "COMPONENT_SET", "ELLIPSE", "SECTION", "POLYGON"]);

const hex = (paints) => {
  if (!Array.isArray(paints)) return null;
  const p = paints.find((p) => p.visible !== false && p.type === "SOLID");
  if (!p) return null;
  const h = (v) => Math.round(v * 255).toString(16).padStart(2, "0");
  const a = p.opacity != null && p.opacity < 0.99 ? "@" + p.opacity.toFixed(2) : "";
  return "#" + h(p.color.r) + h(p.color.g) + h(p.color.b) + a;
};
const hasImage = (paints) => Array.isArray(paints) && paints.some((p) => p.visible !== false && p.type === "IMAGE");
const isArrowCap = (c) => typeof c === "string" && /ARROW|TRIANGLE/.test(c);

function pageFramesOf(container) {
  const out = [];
  for (const n of container.children || []) {
    if (n.visible === false) continue;
    if (n.type === "SECTION") out.push(...pageFramesOf(n));
    else if (n.type === "FRAME" || n.type === "COMPONENT") out.push(n);
  }
  return out;
}
function pageFrameOf(node) {
  let n = node;
  while (n && n.parent && n.parent.type !== "PAGE" && n.parent.type !== "SECTION") n = n.parent;
  return n && (n.type === "FRAME" || n.type === "COMPONENT") ? n : null;
}

let frames = [];
if (root.type === "PAGE" || root.type === "SECTION") frames = pageFramesOf(root);
else {
  const f = pageFrameOf(root) || root;
  frames = [f];
  for (let i = 0; i < frames.length && frames.length < MAX_PAGES; i++) {
    const withReactions = frames[i].findAll((n) => "reactions" in n && n.reactions && n.reactions.length);
    for (const n of withReactions) {
      for (const r of n.reactions) {
        for (const a of r.actions || (r.action ? [r.action] : [])) {
          if (a && a.type === "NODE" && a.destinationId) {
            const d = await figma.getNodeByIdAsync(a.destinationId);
            const df = d && pageFrameOf(d);
            if (df && !frames.includes(df) && frames.length < MAX_PAGES) frames.push(df);
          }
        }
      }
    }
  }
}
const truncated = frames.length >= MAX_PAGES;
frames = frames.slice(0, MAX_PAGES);
const frameById = new Map(frames.map((f) => [f.id, f]));

function readFrame(F) {
  const o = F.absoluteBoundingBox;
  const rel = (b) => ({ x: Math.round(b.x - o.x), y: Math.round(b.y - o.y), w: Math.round(b.width), h: Math.round(b.height) });
  const boxes = [], texts = [], lines = [], links = [];
  const walk = (n) => {
    if (n.visible === false || !n.absoluteBoundingBox) return;
    const b = rel(n.absoluteBoundingBox);
    if ("reactions" in n && n.reactions) {
      for (const r of n.reactions) {
        for (const a of r.actions || (r.action ? [r.action] : [])) {
          if (!a) continue;
          if (a.type === "NODE" && a.destinationId) links.push({ from: n.id, to: a.destinationId, trigger: r.trigger && r.trigger.type });
          if (a.type === "URL") links.push({ from: n.id, url: a.url });
          if (a.type === "BACK") links.push({ from: n.id, back: true });
        }
      }
    }
    if (n.type === "TEXT") {
      const fs = typeof n.fontSize === "number" ? n.fontSize : null;
      const fw = typeof n.fontWeight === "number" ? n.fontWeight : null;
      const t = { id: n.id, k: "text", ...b, text: n.characters, fs, fw };
      if (n.textDecoration === "UNDERLINE") t.underline = true;
      if (n.name && n.name !== n.characters && !DEFAULT_NAME.test(n.name)) t.name = n.name;
      texts.push(t);
      return;
    }
    if (n.type === "LINE" || n.type === "VECTOR") {
      let arrow = isArrowCap(n.strokeCap);
      if (!arrow && n.type === "VECTOR" && n.vectorNetwork) arrow = n.vectorNetwork.vertices.some((v) => isArrowCap(v.strokeCap));
      if (b.w <= 32 && b.h <= 32 && n.type === "VECTOR" && !arrow) {
        boxes.push({ id: n.id, k: "icon", ...b, name: DEFAULT_NAME.test(n.name) ? null : n.name });
      } else lines.push({ id: n.id, ...b, arrow });
      return;
    }
    if (BOXY.has(n.type) && n !== F) {
      const box = { id: n.id, k: n.type.toLowerCase(), ...b };
      if (!DEFAULT_NAME.test(n.name)) box.name = n.name;
      if (n.type === "INSTANCE" && n.mainComponent) box.component = n.mainComponent.name;
      const fill = "fills" in n ? hex(n.fills) : null;
      if (fill) box.fill = fill;
      if ("fills" in n && hasImage(n.fills)) box.image = true;
      const stroke = "strokes" in n ? hex(n.strokes) : null;
      if (stroke) box.stroke = stroke;
      if ("cornerRadius" in n && typeof n.cornerRadius === "number" && n.cornerRadius > 0) box.r = Math.round(n.cornerRadius);
      if (n.type === "ELLIPSE") box.round = true;
      if ("dashPattern" in n && n.dashPattern && n.dashPattern.length) box.dashed = true;
      boxes.push(box);
    }
    if ("children" in n && n.type !== "INSTANCE") for (const c of n.children) walk(c);
    else if (n.type === "INSTANCE") for (const t of n.findAll((x) => x.type === "TEXT" && x.visible !== false)) walk(t);
  };
  for (const c of F.children) walk(c);

  // Merge boxes that share bounds (frame + background rect): keep the first, merge attributes.
  const key = (b) => [b.x, b.y, b.w, b.h].map((v) => Math.round(v / 3)).join(",");
  const seen = new Map(), merged = [];
  for (const b of boxes) {
    const k = key(b);
    if (seen.has(k)) {
      const t = seen.get(k);
      for (const p of ["name", "fill", "image", "stroke", "r", "component", "dashed"]) if (b[p] != null && t[p] == null) t[p] = b[p];
      (t.alsoIds = t.alsoIds || []).push(b.id);
    } else { seen.set(k, b); merged.push(b); }
  }
  // X-placeholder detection: two non-arrow lines spanning a box diagonally.
  const loose = [];
  for (const l of lines) {
    const hit = !l.arrow && l.w > 10 && l.h > 10 && merged.find((b) => Math.abs(b.x - l.x) <= 4 && Math.abs(b.y - l.y) <= 4 && Math.abs(b.w - l.w) <= 4 && Math.abs(b.h - l.h) <= 4);
    if (hit) hit.crossed = (hit.crossed || 0) + 1;
    else if (l.w > 4 && l.h <= 4) merged.push({ id: l.id, k: "hline", ...l });
    else loose.push(l);
  }
  for (const b of merged) if (b.crossed) { b.crossed = b.crossed >= 2; if (b.crossed) b.image = true; }

  // Geometric nesting.
  const area = (b) => b.w * b.h;
  const inside = (a, b) => a.x >= b.x - TOL && a.y >= b.y - TOL && a.x + a.w <= b.x + b.w + TOL && a.y + a.h <= b.y + b.h + TOL;
  const all = [...merged, ...texts];
  const sortedBoxes = [...merged].filter((b) => b.k !== "hline" && b.k !== "icon").sort((a, b) => area(a) - area(b));
  const rootNode = { children: [] };
  for (const el of all) {
    const parent = sortedBoxes.find((b) => b !== el && area(b) > area(el) && inside(el, b));
    el._p = parent || rootNode;
  }
  for (const el of all) (el._p.children = el._p.children || []).push(el);
  const order = (list) => {
    list.sort((a, b) => a.y - b.y);
    const rows = [];
    for (const el of list) {
      const row = rows.find((r) => el.y < r.bottom - Math.min(el.h, r.minH) * 0.5);
      if (row) { row.items.push(el); row.bottom = Math.max(row.bottom, el.y + el.h); row.minH = Math.min(row.minH, el.h); }
      else rows.push({ items: [el], bottom: el.y + el.h, minH: el.h });
    }
    return rows.flatMap((r) => r.items.sort((a, b) => a.x - b.x));
  };
  const strip = (el) => {
    delete el._p;
    if (el.children) { el.children = order(el.children).map(strip); if (!el.children.length) delete el.children; }
    return el;
  };
  const tree = order(rootNode.children).map(strip);
  return {
    id: F.id, name: F.name, w: Math.round(F.width), h: Math.round(F.height),
    fill: hex(F.fills), tree, links, looseLines: loose.length ? loose : undefined,
  };
}

const pages = frames.map(readFrame);

// Canvas-level arrows (drawn between frames): resolve each end to a frame + element.
const arrows = [];
const containerOfFrames = frames[0] && frames[0].parent;
const canvasNodes = containerOfFrames ? containerOfFrames.findAll((n) => (n.type === "LINE" || n.type === "VECTOR") && !pageFrameOf(n)) : [];
const endpoints = (n) => {
  const t = n.absoluteTransform;
  if (n.type === "LINE") return [{ x: t[0][2], y: t[1][2] }, { x: t[0][2] + t[0][0] * n.width, y: t[1][2] + t[1][0] * n.width }];
  const vs = n.vectorNetwork ? n.vectorNetwork.vertices : [];
  if (vs.length < 2) return null;
  const tr = (v) => ({ x: t[0][0] * v.x + t[0][1] * v.y + t[0][2], y: t[1][0] * v.x + t[1][1] * v.y + t[1][2] });
  return [tr(vs[0]), tr(vs[vs.length - 1])];
};
const locate = (p) => {
  const f = frames.find((F) => { const b = F.absoluteBoundingBox; return p.x >= b.x && p.x <= b.x + b.width && p.y >= b.y && p.y <= b.y + b.height; });
  if (!f) {
    // Nearest frame within 120 px (arrow heads often stop just short of a frame).
    let best = null, bd = 120;
    for (const F of frames) {
      const b = F.absoluteBoundingBox;
      const dx = Math.max(b.x - p.x, 0, p.x - (b.x + b.width)), dy = Math.max(b.y - p.y, 0, p.y - (b.y + b.height));
      const d = Math.hypot(dx, dy);
      if (d < bd) { bd = d; best = F; }
    }
    return best ? { frame: best.name, near: true } : null;
  }
  const o = f.absoluteBoundingBox;
  const hits = f.findAll((n) => n.visible !== false && n.absoluteBoundingBox && n.type !== "LINE" && n.type !== "VECTOR" && (() => { const b = n.absoluteBoundingBox; return p.x >= b.x && p.x <= b.x + b.width && p.y >= b.y && p.y <= b.y + b.height; })());
  hits.sort((a, b) => a.absoluteBoundingBox.width * a.absoluteBoundingBox.height - b.absoluteBoundingBox.width * b.absoluteBoundingBox.height);
  return { frame: f.name, element: hits[0] ? hits[0].id : null, at: { x: Math.round(p.x - o.x), y: Math.round(p.y - o.y) } };
};
for (const n of canvasNodes) {
  if (n.visible === false) continue;
  const ep = endpoints(n);
  if (!ep) continue;
  let capStart = null, capEnd = null;
  if (n.type === "VECTOR" && n.vectorNetwork) {
    const vs = n.vectorNetwork.vertices;
    capStart = vs[0].strokeCap; capEnd = vs[vs.length - 1].strokeCap;
  } else capEnd = n.strokeCap;
  const hasArrow = isArrowCap(capStart) || isArrowCap(capEnd) || isArrowCap(n.strokeCap);
  if (!hasArrow && !/pfeil|arrow|→/i.test(n.name)) continue;
  let [a, b] = ep;
  if (isArrowCap(capStart) && !isArrowCap(capEnd)) [a, b] = [b, a];
  arrows.push({ id: n.id, from: locate(a), to: locate(b) });
}

// Resolve prototype link destinations to frame names.
for (const p of pages) {
  for (const l of p.links) {
    if (!l.to) continue;
    const d = await figma.getNodeByIdAsync(l.to);
    const df = d && pageFrameOf(d);
    l.toFrame = df ? df.name : null;
    l.toFrameInSketch = !!(df && frameById.has(df.id));
  }
  if (!p.links.length) delete p.links;
}

return {
  file: figma.root.name, page: pg ? pg.name : null, target: root.name, targetType: root.type,
  pages, arrows, truncated,
  notes: truncated ? "Only the first " + MAX_PAGES + " frames were read." : undefined,
};
