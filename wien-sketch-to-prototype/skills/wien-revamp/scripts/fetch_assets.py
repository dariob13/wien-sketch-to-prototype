#!/usr/bin/env python3
"""Official Stadt Wien icons (pictograms) and illustrations: catalog + search.

The ONLY icons and illustrations the workflow may choose come from:
  https://handbuch.wien.gv.at/look-and-feel/icons-und-illustrationen/icons/
  https://handbuch.wien.gv.at/look-and-feel/icons-und-illustrationen/illustrationen/

Usage:
  python3 -I fetch_assets.py --refresh               # rebuild both catalogs in ../references/
  python3 -I fetch_assets.py icons schwimmen         # search pictograms (name, category, keywords)
  python3 -I fetch_assets.py illustrationen bad      # search illustrations
  python3 -I fetch_assets.py icons --all             # list everything

Search reads the cached TSV catalogs (references/icon-catalog.tsv,
references/illustration-catalog.tsv). Run --refresh when the handbook changes;
selfcheck.py reports when the cache is out of date. Standard library only.
"""
import argparse
import html
import pathlib
import re
import sys
import unicodedata
import urllib.request

BASE = "https://handbuch.wien.gv.at"
PAGES = {
    "icons": BASE + "/look-and-feel/icons-und-illustrationen/icons/",
    "illustrationen": BASE + "/look-and-feel/icons-und-illustrationen/illustrationen/",
}
REF = pathlib.Path(__file__).resolve().parent.parent / "references"
CATALOG = {"icons": REF / "icon-catalog.tsv", "illustrationen": REF / "illustration-catalog.tsv"}
UA = "wien-sketch-to-prototype/1.0 (asset catalog)"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def text(s):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s))).strip()


def parse(page):
    rows = []
    for body in re.findall(r'<tr id="icon_[^"]+"[^>]*>(.*?)</tr>', page, re.S):
        src = re.search(r'<img src="([^"]+\.svg)"', body)
        name = re.search(r"<strong>(.*?)</strong>", body, re.S)
        tds = re.findall(r"<td>(.*?)</td>", body, re.S)
        if not (src and name and len(tds) >= 4):
            continue
        kw = re.sub(r'<span class="wm-h-vh">.*?</span>', "", tds[3], flags=re.S)
        rows.append({
            "name": text(name.group(1)),
            "category": text(tds[2]),
            "keywords": text(kw).strip(" ,"),
            "url": BASE + src.group(1) if src.group(1).startswith("/") else src.group(1),
        })
    return rows


def fold(s):
    s = s.lower().replace("ß", "ss")
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))


def load(kind):
    path = CATALOG[kind]
    if not path.exists():
        sys.exit(f"No catalog at {path}. Run: python3 -I {pathlib.Path(__file__).name} --refresh")
    lines = path.read_text(encoding="utf-8").splitlines()
    head = lines[0].split("\t")
    return [dict(zip(head, l.split("\t"))) for l in lines[1:] if l.strip()]


def refresh():
    for kind, url in PAGES.items():
        rows = parse(get(url))
        if not rows:
            sys.exit(f"{kind}: no rows parsed from {url}. The page structure changed; fix parse().")
        out = ["name\tcategory\tkeywords\turl"] + [
            "\t".join(r[k].replace("\t", " ") for k in ("name", "category", "keywords", "url")) for r in rows]
        CATALOG[kind].write_text("\n".join(out) + "\n", encoding="utf-8")
        print(f"{kind}: {len(rows)} entries → {CATALOG[kind].relative_to(REF.parent)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", nargs="?", choices=sorted(PAGES))
    ap.add_argument("query", nargs="*")
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    if a.refresh:
        refresh()
        return
    if not a.kind:
        ap.error("give icons|illustrationen and a search word, or --refresh")
    rows = load(a.kind)
    if not a.all:
        words = [fold(w) for w in a.query]
        if not words:
            ap.error("give a search word or --all")
        scored = []
        for r in rows:
            name, rest = fold(r["name"]), fold(r["category"] + " " + r["keywords"])
            score = sum(3 if w in name else 1 if w in rest else 0 for w in words)
            if score and all(w in name or w in rest for w in words):
                scored.append((-score, r["name"], r))
        rows = [r for _, _, r in sorted(scored)]
    if not rows:
        print("Kein Treffer. Nichts erfinden: Icon weglassen bzw. Bild-Platzhalter verwenden und im Report melden.")
        return
    for r in rows[:40]:
        print(f'{r["name"]}\t{r["category"]}\t{r["url"]}')
    if len(rows) > 40:
        print(f"… {len(rows) - 40} more (narrow the search)")


if __name__ == "__main__":
    main()
