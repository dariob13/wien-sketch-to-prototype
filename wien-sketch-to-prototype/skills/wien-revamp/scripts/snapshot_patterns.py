#!/usr/bin/env python3
"""Maintainer tool: save an offline copy of the handbook samples into the skill.

The Claude app (claude.ai, Desktop) runs skills in a sandbox that may not reach
handbuch.wien.gv.at. The skill then reads these files instead of fetching live.

Run after every theme release (selfcheck.py tells you when):
  python3 -I snapshot_patterns.py

Writes references/samples/<slug>.html (every variant, header compacted) and
references/samples/INDEX.md (slug, variants, theme version, date).
Standard library only.
"""
import datetime
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fetch_pattern as fp  # noqa: E402

REF = HERE.parent / "references"
OUT = REF / "samples"


def slugs():
    """Every slug in pattern-index.md that is not a form/app pattern (v1 scope)."""
    idx = (REF / "pattern-index.md").read_text(encoding="utf-8")
    out = []
    section = ""
    for line in idx.splitlines():
        if line.startswith("## "):
            section = line[3:].strip().lower()
        m = re.match(r"\|\s*[^|]+\|\s*`([^`]+)`\s*\|", line)
        if m and not section.startswith("forms"):
            out.append(m.group(1))
    return sorted(set(out))


def main():
    version = fp.theme_version() or "unknown"
    today = datetime.date.today().isoformat()
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.html"):
        old.unlink()
    rows = []
    for slug in slugs():
        try:
            url, vs = fp.variants(slug)
        except Exception as e:  # 404 or network
            print(f"skip {slug}: {e}")
            continue
        if not vs:
            print(f"skip {slug}: no samples")
            continue
        parts = [f"<!-- Snapshot of {url} · theme v{version} · {today} -->"]
        for n, v in enumerate(vs):
            html = fp.compact(v["html"], slug == "header") if slug == "header" else v["html"]
            parts.append(f"<!-- Source: {v['source']} — variant {n}: {v['name']} -->\n{html}\n")
        name = slug.replace("/", "_")
        (OUT / f"{name}.html").write_text("\n".join(parts), encoding="utf-8")
        rows.append(f"| `{slug}` | `samples/{name}.html` | " + " · ".join(f"{n}: {v['name']}" for n, v in enumerate(vs)) + " |")
        print(f"ok   {slug} ({len(vs)} variants)")
    index = [
        "# Offline pattern samples",
        "",
        f"Snapshot of handbuch.wien.gv.at, theme **v{version}**, taken {today}.",
        "Use these files only when a live fetch is not possible (see handbuch-fetch.md).",
        "Each file holds every variant of one pattern, each starting with a `<!-- Source: … — variant n: … -->` line.",
        "",
        "| Slug | File | Variants |",
        "| --- | --- | --- |",
        *rows,
        "",
    ]
    (OUT / "INDEX.md").write_text("\n".join(index), encoding="utf-8")
    print(f"\n{len(rows)} patterns → {OUT}")


if __name__ == "__main__":
    main()
