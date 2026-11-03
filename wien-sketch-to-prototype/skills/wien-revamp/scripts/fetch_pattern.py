#!/usr/bin/env python3
"""Print the copyable sample markup of a Wiener Melange handbook pattern.

Usage:
  python3 -I fetch_pattern.py <slug> --list            # variant names only
  python3 -I fetch_pattern.py <slug>                   # every variant
  python3 -I fetch_pattern.py <slug> --variant "farbig mit Text"
  python3 -I fetch_pattern.py <slug> --index 0         # the unheaded default sample
  python3 -I fetch_pattern.py --version                # current theme version

Standard library only. Reads https://handbuch.wien.gv.at/pattern-library/patterns/<slug>/,
takes the inner HTML of each "Vorschau" panel (wm-tabpanel.code-preview-rendered),
makes root-relative URLs absolute, and resolves "… öffnen" template links
(e.g. the header) to the real element on the template page.

A page with no Vorschau panels (suche) is read from its Varianten tab instead:
each h3's first link to a pattern or template becomes a sample under that h3's
name. For a list of header templates the wien.gv.at standard header is used,
not a Sonderauftritt. A section that only links off-site is skipped.
"""
import argparse
import html
import re
import sys
import urllib.request

BASE = "https://handbuch.wien.gv.at"
UA = "wien-sketch-to-prototype/1.0 (pattern fetch)"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def balanced(src, start, tag):
    """Return the end index just after the element <tag ...> opened at src[start]."""
    depth = 0
    pat = re.compile(r"<(/?)%s\b[^>]*>" % re.escape(tag), re.I)
    for m in pat.finditer(src, start):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return m.end()
    return len(src)


def absolutize(s):
    s = re.sub(r'(\s(?:src|href|poster|data-src)=")/(?!/)', r"\1" + BASE + "/", s)

    def fix_srcset(m):
        parts = [p.strip() for p in m.group(2).split(",")]
        parts = [BASE + p if p.startswith("/") and not p.startswith("//") else p for p in parts]
        return m.group(1) + ", ".join(parts) + '"'

    return re.sub(r'(\ssrcset=")([^"]*)"', fix_srcset, s)


def clean(s):
    s = re.sub(r"\n\s*\n+", "\n", s.strip())
    # Demo-only attributes and known typos in handbook samples (checked 2026-11-03).
    s = re.sub(r'\s+data-demo-pattern="[^"]*"', "", s)
    s = re.sub(r'(<wm-tag-list\b[^>]*?)\s+scrollable"', r"\1 scrollable", s)
    return s


def template_markup(page_html, slug):
    """Markup to keep from a handbook template page (a whole demo page)."""
    b0 = page_html.find("<body")
    tb = page_html[b0:] if b0 >= 0 else page_html
    tb = re.sub(r"<script\b.*?</script>", "", tb, flags=re.S)
    tb = re.sub(r"<main>\s*</main>", "", tb)
    tb = re.sub(r"^<body[^>]*>|</body>.*$", "", tb, flags=re.S)
    slug = slug.strip("/")
    # For any pattern other than the header, keep only <main>, minus the demo stage.
    m_main = re.search(r"<main\b[^>]*>(.*)</main>", tb, re.S)
    if slug != "header" and m_main and m_main.group(1).strip():
        tb = m_main.group(1)
        if slug != "stage":
            tb = re.sub(r"<wm-stage\b.*?</wm-stage>", "", tb, count=1, flags=re.S)
    elif slug == "header":
        mh = re.search(r"<wm-header\b.*?</wm-header>", tb, re.S)
        tb = mh.group(0) if mh else tb
    return tb


def variants(slug, follow=True):
    url = "%s/pattern-library/patterns/%s/" % (BASE, slug.strip("/"))
    page = get(url)
    i = page.find("pl-samples")
    body = page[i:] if i >= 0 else page
    out = []
    last_end = 0
    for m in re.finditer(r'<wm-tabpanel\b[^>]*class="[^"]*code-preview-rendered[^"]*"[^>]*>', body):
        if m.start() < last_end:
            continue  # nested inside the previous sample
        end = balanced(body, m.start(), "wm-tabpanel")
        inner = body[m.end():end - len("</wm-tabpanel>")]
        before = body[last_end:m.start()]
        heads = re.findall(r"<wm-anchor\b[^>]*>\s*<h3[^>]*>(.*?)</h3>", before, re.S)
        name = html.unescape(re.sub(r"<[^>]+>", "", heads[-1]).strip()) if heads else "(Standard – ohne Überschrift)"
        last_end = end
        tmpl = re.fullmatch(r'\s*<wm-cta>\s*<a href="(/pattern-library/templates/[^"]+)">[^<]*</a>\s*</wm-cta>\s*', inner)
        source = url
        if tmpl:
            source = BASE + tmpl.group(1)
            inner = template_markup(get(source), slug)
        out.append({"name": name, "html": clean(absolutize(inner)), "source": source})
    if not out and follow:
        out = linked_samples(page, slug.strip("/"))
    return url, out


def linked_samples(page, slug):
    """No Vorschau panels: one sample per Varianten h3 that links to a pattern or template."""
    m = re.search(
        r"<wm-tab\b[^>]*>\s*Varianten\s*</wm-tab>\s*<wm-tabpanel\b[^>]*>(.*?)</wm-tabpanel>",
        page, re.S)
    if not m:
        return []
    pieces = re.split(r"(<h3\b[^>]*>.*?</h3>)", m.group(1), flags=re.S)
    samples = []
    i = 1
    while i + 1 < len(pieces):
        name = html.unescape(re.sub(r"<[^>]+>", "", pieces[i])).strip()
        chunk = pieces[i + 1]
        i += 2
        links = re.findall(r'href="(/pattern-library/(?:patterns|templates)/[^"#]+)"', chunk)
        href = pick_link(links, slug)
        if not href:
            continue
        sample = sample_from_href(href, name)
        if sample:
            samples.append(sample)
    return samples


def pick_link(links, slug):
    if not links:
        return None
    # A content page uses the standard header. The other header links are Sonderauftritte.
    if any("/header/" in h for h in links):
        for h in links:
            if h.rstrip("/").endswith("/header/standard"):
                return h
    self_pat = re.compile(r"/patterns/%s/?$" % re.escape(slug))
    for h in links:
        if not self_pat.search(h):
            return h
    return None


def sample_from_href(href, name):
    source = BASE + href
    if "/templates/" in href:
        kind = "header"
        m = re.search(r"/templates/patterns/([^/]+)/", href)
        if m:
            kind = m.group(1)
        inner = template_markup(get(source), kind)
        if not inner.strip():
            return None
        return {"name": name, "html": clean(absolutize(inner)), "source": source}
    m = re.search(r"/patterns/([^/]+)/?$", href)
    if not m:
        return None
    _, vs = variants(m.group(1), follow=False)
    if not vs:
        return None
    return {"name": name, "html": vs[0]["html"], "source": vs[0]["source"]}


def theme_version():
    page = get(BASE + "/development/erste-schritte/")
    m = re.search(r"Die aktuelle Version ist[^0-9v]*v?(\d+\.\d+\.\d+)", re.sub(r"<[^>]+>", " ", page))
    if m:
        return m.group(1)
    vs = re.findall(r"theme/v(\d+\.\d+\.\d+)/", page)
    return max(vs, key=lambda v: tuple(map(int, v.split(".")))) if vs else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="?")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--variant")
    ap.add_argument("--index", type=int)
    ap.add_argument("--version", action="store_true")
    ap.add_argument("--compact", action="store_true",
                    help="collapse whitespace; for the header also drop nested demo submenus")
    a = ap.parse_args()
    if a.version:
        print(theme_version() or "unknown")
        return
    if not a.slug:
        ap.error("slug required")
    url, vs = variants(a.slug)
    if not vs:
        print("No samples found on %s – open the page and check the slug." % url, file=sys.stderr)
        sys.exit(2)
    if a.list:
        for n, v in enumerate(vs):
            print("%2d  %s" % (n, v["name"]))
        return
    sel = list(enumerate(vs))
    if a.index is not None:
        sel = [p for p in sel if p[0] == a.index]
    if a.variant:
        q = a.variant.lower()
        sel = [p for p in sel if q in p[1]["name"].lower()]
    if not sel:
        print("No variant matched. Use --list.", file=sys.stderr)
        sys.exit(3)
    for n, v in sel:
        out = v["html"]
        if a.compact:
            out = compact(out, a.slug.strip("/") == "header")
        print("<!-- Source: %s — variant %d: %s -->" % (v["source"], n, v["name"]))
        print(out)
        print()


def compact(s, is_header):
    if is_header:
        # Keep logo, search, menu button, language/service lists and first-level
        # menu items; drop the nested demo submenus (hidden until the menu opens).
        def strip_nested(m):
            block = m.group(0)
            # Remove every <ul> that directly follows a menu item's link.
            while True:
                mm = re.search(r"(<li>\s*<a[^>]*>[^<]*(?:<wm-icon[^>]*></wm-icon>)?[^<]*</a>\s*)<ul>", block)
                if not mm:
                    break
                start = mm.end() - len("<ul>")
                end = balanced(block, start, "ul")
                block = block[:start] + block[end:]
            return block
        s = re.sub(r"<wm-nav-main\b.*?</wm-nav-main>", strip_nested, s, flags=re.S)
    s = re.sub(r">\s+<", "><", s)
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip()


if __name__ == "__main__":
    main()
