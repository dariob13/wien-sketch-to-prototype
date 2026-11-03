#!/usr/bin/env python3
"""Maintainer check: does the workflow still match the live handbook?

Run:  python3 -I wien-sketch-to-prototype/skills/wien-revamp/scripts/selfcheck.py

Checks
  1. Theme version on handbuch.wien.gv.at vs. the version pinned in page-shell.md.
  2. Every pattern slug referenced in tag-vocabulary.md still has samples.
  3. Every quoted variant name in tag-vocabulary.md still exists on its pattern page.
  4. The header and Vorspann template links still resolve to real markup.
  5. Every tag in docs/cheat-sheet.md is known to tag-vocabulary.md.

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

# 2 + 3. slugs and variant names from the vocabulary tables
vocab = (REF / "tag-vocabulary.md").read_text(encoding="utf-8")
rows = [l for l in vocab.splitlines() if l.startswith("|") and "`" in l]
by_slug = {}
for row in rows:
    cells = [c.strip() for c in row.strip("|").split("|")]
    slug_cells = [c for c in cells if re.fullmatch(r"`[a-z0-9/-]+`", c)]
    if not slug_cells:
        continue
    slug = slug_cells[0].strip("`")
    names = re.findall(r'"([^"]+?)"', row.replace('\\"', "\u0000"))
    names = [n.replace("\u0000", '"') for n in names]
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

for n in notes:
    print("ok   ", n)
for p in problems:
    print("FIX  ", p)
print("\nAll good." if not problems else f"\n{len(problems)} thing(s) to fix.")
sys.exit(1 if problems else 0)
