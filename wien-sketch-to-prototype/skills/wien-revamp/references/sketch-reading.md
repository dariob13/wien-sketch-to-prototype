# Reading a sketch

The goal is one **page outline** per sketched page, the same shape whether the sketch came from Figma or Doop:

```
Page "Startseite" (Figma frame 12:3, sketched at 1440)
  1. [Bühne]          box 12:7  → stage            tag     "Baden in Wien" / "Alle Bäder auf einen Blick"
  2. (untagged)       box 12:9  → tag list         guess   pills: "Hallenbäder", "Freibäder", "← Freizeit"
  3. [Karten x3 Bild] box 12:14 → card ×3 (grid)   tag     … per card: title, text, image, → "Bad-Detail"
  4. [Abschnitt grau] box 12:30 → section (bg)     tag     children: [Quicklinks] …
  -  [Notiz]          box 12:41 → instruction      —       "Link-Ziele kommen noch"
  Links: card 1 → "Bad-Detail" (prototype link)
```

Keep the element ids. You need them for the report, and for the comment you leave when something is unclear.

## Which frames are pages

- **Figma:** every top-level frame on the linked page, or in the linked section, is one sketched page. A link to a single frame means that page plus the frames its prototype links lead to.
- **Doop:** every frame on the linked canvas page is one sketched page, except frames named `Referenz…`, `… – Mobil`, `… – Desktop` and frames on a page called `Prototyp`, which are output. A `?frame=` link means that frame plus the frames it links to (`data-doop-action="navigate:…"`).
- The frame name is the page name. Links like `→ Bad-Detail` match frame names, using the same forgiving rules as tags.
- A frame named `[Notiz] …`, `Legende`, `Spickzettel`, `Cheat Sheet`, or `Vorlage …` is not a page. Skip it.
- Sketch width does not matter. A 375-wide sketch and a 1440-wide sketch both produce Mobil and Desktop. Side-by-side boxes in a 375 sketch still mean columns on desktop.

## Figma

1. Parse the URL: `figma.com/design/<fileKey>/…?node-id=1-2` → fileKey, nodeId `1:2`. If there is no `node-id`, call `get_metadata` without a nodeId, list the pages, and ask which one (or take the only page with frames).
2. `create_session` with the file key and the task "Read sketch for Wiener Melange prototype".
3. Load the `figma-use` skill if your client has it (Claude Code requires it before `use_figma`). Read [../scripts/figma-read-sketch.js](../scripts/figma-read-sketch.js), replace `__NODE_ID__`, and run it with `use_figma` (`skillNames: "figma-use"`). It is read-only and returns the frames, a box tree nested by geometry, texts with font size and weight, prototype links, and arrows drawn between frames.
4. `get_screenshot` on each page frame (or on the section) at `maxDimension` 1600. Look at it. The script gives you structure, and the screenshot gives you intent: hand-drawn X placeholders, arrows drawn with the pen, which box is visually "the big one at the top".
5. If the script fails, fall back to `get_metadata` (structure) plus the screenshot. Text then comes from layer names, so say in the report that the text may be incomplete.

Never write to the sketch file. Questions go into the chat.

## Doop

1. Parse the URL: `doop.design/c/<canvas_id>?frame=<frame_id>`. Call `get_guide` (`doop-instructions`) once per session, then `get_canvas` with your `agent_name`.
2. `get_frame` for each sketch frame (HTML), and `get_frame_screenshot` for each.
3. Read the HTML as a box tree: elements with a border, a background, or a fixed size are boxes, and their text is content. Keep `data-doop-id` as the element id. Existing `data-doop-on`/`data-doop-action="navigate:<frameId>"` attributes are links, so resolve the frame id to a frame name via `get_canvas`.
4. Use the screenshot the same way as in Figma.

## Untagged boxes

Guess from shape, position, and content. Every guess gets a basis in the report: **tag** (written by the sketcher), **likely** (the shape rule fits clearly), or **unsure** (nothing fits well, or two rules compete). Never present a guess as if it had been tagged.

| What you see | Likely pattern |
| --- | --- |
| Full-width thin bar at the very top (under ~120 px tall at 1440, or the first box) | Header |
| Full-width box at the very bottom, small text, many short links | Footer |
| The first big box under the header, containing the page's largest text | Stage. If it also has an image/X → stage with image. |
| A row of small pill or rounded boxes with one or two words each | Tag list. A pill starting with `←`/`<` → parent-channel tag. |
| 2–4 equal boxes side by side, each with a heading and text | Cards, with the count as columns |
| The same, each with an image/X at the top | Teaser cards with images |
| A row of equal boxes running off the right edge, or with `<` `>` / dots | Carousel |
| A box with several short lines ending in `→`, `>`, `›` | Quicklinks |
| Text lines starting with `-`, `•`, numbers | List |
| A grid of text separated by lines, or text aligned in columns | Table |
| Stacked rows with `+`, `▸`, `▾`, or chevrons at one side | Accordion |
| A small box with short text, filled or outlined, radius > 0, under ~60 px tall | Button. With an arrow and no fill → Mehr-Link. |
| A full-width band with a grey/colored fill containing other boxes | Section with background |
| A box with an X, a picture fill, or the word Bild/Foto | Image |
| A box with a pin, "Stadtplan", or an address | Map placeholder |
| A box with a name, phone, email, address near the end of the page | Contact |
| A horizontal line between blocks | Divider |
| A box with a heading and a paragraph that fits none of the above | Plain section (H2 + text). Mark it **unsure** if it looks like it was meant to be something more. |

A text that is not inside any box sits directly in the page: a large one becomes an H2 section heading, a normal one body text in a section.

If two rules compete (three equal boxes might be cards or quicklinks), pick one, mark it **unsure**, and give the alternative.

## Links (click-through)

Sources, strongest first:

1. **Figma prototype connections** (`links` in the script output, `toFrame`). Doop: existing `data-doop-action="navigate:…"`.
2. **Text in the box**: `→ Seitenname`, `-> Seitenname`, `link: Seitenname`. On a line of its own it links the whole box. At the end of a line it links that line's item.
3. **Exact page names**: a tag, quicklink, or list item whose text is exactly the name of another sketched page (ignoring `←`/`→` and case) links there. Basis `Erkannt ~`.
4. **Drawn arrows** between frames (`arrows` in the script output, or pen arrows seen in the screenshot). The `from` element is the trigger and the `to` frame is the target. Hand-drawn arrows are **likely** at best. If `from` is a whole box, the trigger is the link line in that box closest to the arrow's start (`at.y`). For `directionGuessed` arrows, check the screenshot.

Every link target must be a sketched page. A target that is not, such as `→ Kontaktseite` with no such frame, gets `[Link-Ziel fehlt: Kontaktseite]` in the report and a dead link (`href="#"`) in the build. `→ https://…` is an external link: keep the `href` and wire `data-doop-action="url:…"`.

An arrow or link with no clear trigger element (it starts on empty space) links nothing. Report it.

## Before you map: things to flag

- Text that overflows its box or overlaps another box. Ask which box it belongs to only if it changes the result.
- Boxes that overlap each other without nesting. The topmost one (the later layer) wins; report it.
- A page with no stage or H1. Build it anyway, and recommend a stage in the report.
- More than one stage, or more than one H1 on a page. Keep the first as the stage; the next ones become sections with H2.
