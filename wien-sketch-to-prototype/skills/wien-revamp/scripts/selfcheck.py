#!/usr/bin/env python3
"""Maintainer check: does the workflow still match the live handbook?

Run:  python3 -I wien-sketch-to-prototype/skills/wien-revamp/scripts/selfcheck.py

Checks
  1. Theme version on handbuch.wien.gv.at vs. the version pinned in page-shell.md.
  2. Every slug in the "Pattern (slug)" column of tag-vocabulary.md still has samples.
  3. Every quoted variant name in tag-vocabulary.md still exists on its pattern page.
     A quote counts only when it starts with an uppercase letter and is not a
     section title of tag-vocabulary.md (so "full", "nebelgrau" and "Text with
     no slot" are not variant names). A pattern cell that lists several slugs
     is an existence check only.
  4. The header and Vorspann template links still resolve to real markup.
  5. Every tag in docs/cheat-sheet.md is known to tag-vocabulary.md.
  6. The icon and illustration catalogs match the handbook pages.
  7. The offline sample snapshot has the live theme version.

Exit code 0 = all good, 1 = something to fix (details printed).
Standard library only; imports fetch_pattern.py from the same folder.
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fetch_pattern as fp  # noqa: E402

REF = HERE.parent / "references"
DOCS = HERE.parents[2] / "docs"
problems, notes = [], []


def norm(s):
    return re.sub(r"\s+", " ", s.replace("&quot;", '"').replace("\\\"", '"')).strip().lower()


SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"
SLUG_CELL = re.compile(r"`%s`(?:\s*[·,/]\s*`%s`)*" % (SLUG, SLUG))


def section_titles(text):
    """Headings and bold lead-ins, so a doc cross-reference is not a variant name."""
    titles = set()
    for m in re.finditer(r"^#{1,6}\s+(.+?)\s*$", text, re.M):
        titles.add(norm(m.group(1)).strip(" ."))
    for m in re.finditer(r"^(?:>\s*)?\*\*([^*]+)\*\*", text, re.M):
        titles.add(norm(m.group(1)).strip(" ."))
    return titles


def variant_quotes(row, titles):
    raw = re.findall(r'"([^"]+?)"', row.replace('\\"', "\u0000"))
    names = []
    for n in raw:
        n = n.replace("\u0000", '"').strip()
        if not n[:1].isupper():
            continue
        if norm(n).strip(" .") in titles:
            continue
        names.append(n)
    return names


# 1. theme version
shell = (REF / "page-shell.md").read_text(encoding="utf-8")
pinned = sorted(set(re.findall(r"theme/v(\d+\.\d+\.\d+)/", shell)))
live = fp.theme_version()
if not live:
    problems.append("Could not read the current theme version from the handbook.")
elif pinned != [live]:
    problems.append(f"Theme version: handbook says v{live}, page-shell.md pins {pinned}. Update page-shell.md, foundations.md and the cached notes.")
else:
    notes.append(f"Theme v{live} matches page-shell.md.")

# 2 + 3. slugs and variant names from the vocabulary tables.
# Only the "Pattern (slug)" column counts. Other columns list modifiers
# (`hell`, `light`), and those words are not pattern pages.
vocab = (REF / "tag-vocabulary.md").read_text(encoding="utf-8")
titles = section_titles(vocab)
by_slug = {}
header = None
for line in vocab.splitlines():
    if not line.startswith("|"):
        header = None
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if cells and all(re.fullmatch(r":?-+:?", c) for c in cells):
        continue
    if header is None:
        header = cells
        continue
    if "Pattern (slug)" not in header:
        continue
    idx = header.index("Pattern (slug)")
    if idx >= len(cells) or not SLUG_CELL.fullmatch(cells[idx]):
        continue
    slugs = re.findall(r"`(%s)`" % SLUG, cells[idx])
    # One slug owns the row's variant names. Several slugs are only "does this page exist".
    names = variant_quotes(line, titles) if len(slugs) == 1 else []
    for slug in slugs:
        by_slug.setdefault(slug, set()).update(names)

for slug, names in sorted(by_slug.items()):
    try:
        _, vs = fp.variants(slug)
    except Exception as e:  # network or 404
        problems.append(f"{slug}: page could not be fetched ({e}).")
        continue
    if not vs:
        problems.append(f"{slug}: no samples found.")
        continue
    live_names = [norm(v["name"]) for v in vs]
    for n in sorted(names):
        key = norm(n).replace("…", "").strip()
        if key.endswith("version") or len(key) < 4:
            continue
        if not any(key in ln for ln in live_names):
            problems.append(f'{slug}: variant "{n}" not found on the pattern page (renamed?).')
notes.append(f"Checked {len(by_slug)} pattern slugs from tag-vocabulary.md.")

# 4. template-based samples
_, hv = fp.variants("header")
if not hv or not hv[0]["html"].lstrip().startswith("<wm-header"):
    problems.append("header: sample 0 no longer resolves to <wm-header> (template link changed?).")
_, vv = fp.variants("vorspann")
if not any("wm-teaser-text" in v["html"] for v in vv):
    problems.append("vorspann: no sample contains p.wm-teaser-text any more.")

# 5. cheat-sheet tags known to the vocabulary
cheat = (DOCS / "cheat-sheet.md").read_text(encoding="utf-8")
vocab_l = vocab.lower()
for tag in sorted(set(re.findall(r"^\| `\[([^\]\s]+)[^\]]*\]`", cheat, re.M))):
    if tag.lower() not in vocab_l and tag not in ("?",):
        problems.append(f"cheat-sheet tag [{tag}] does not appear in tag-vocabulary.md.")

# 6. icon and illustration catalogs match the handbook pages
import fetch_assets as fa  # noqa: E402
for kind in ("icons", "illustrationen"):
    try:
        live_rows = fa.parse(fa.get(fa.PAGES[kind]))
        cached = fa.load(kind)
    except SystemExit as e:
        problems.append(f"{kind}: {e}")
        continue
    except Exception as e:
        problems.append(f"{kind}: page could not be fetched ({e}).")
        continue
    live_set = {(r["name"], r["url"]) for r in live_rows}
    cache_set = {(r["name"], r["url"]) for r in cached}
    if not live_rows:
        problems.append(f"{kind}: no entries parsed from the handbook page (structure changed? fix fetch_assets.parse).")
    elif live_set != cache_set:
        problems.append(f"{kind}: catalog out of date (+{len(live_set - cache_set)} / -{len(cache_set - live_set)}). Run: python3 -I scripts/fetch_assets.py --refresh")
    else:
        notes.append(f"{kind}: catalog matches the handbook ({len(cached)} entries).")

# 7. offline sample snapshot matches the live theme version
snap = REF / "samples" / "INDEX.md"
if not snap.exists():
    problems.append("No offline snapshot (references/samples). Run: python3 -I scripts/snapshot_patterns.py")
else:
    m = re.search(r"theme \*\*v(\d+\.\d+\.\d+)\*\*, taken ([0-9-]+)", snap.read_text(encoding="utf-8"))
    if not m:
        problems.append("references/samples/INDEX.md has no theme version line.")
    elif live and m.group(1) != live:
        problems.append(f"Offline snapshot is theme v{m.group(1)}, handbook is v{live}. Run: python3 -I scripts/snapshot_patterns.py")
    else:
        notes.append(f"Offline snapshot: theme v{m.group(1)}, taken {m.group(2)}.")

for n in notes:
    print("ok   ", n)
for p in problems:
    print("FIX  ", p)
print("\nAll good." if not problems else f"\n{len(problems)} thing(s) to fix.")
sys.exit(1 if problems else 0)
