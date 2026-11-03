#!/usr/bin/env python3
"""Render docs/cheat-sheet.md to a printable A4 HTML page (docs/cheat-sheet.html).

The same HTML is used for the "Spickzettel" frame in the Doop starter canvas.
Standard library only; supports the Markdown subset the cheat sheet uses.
Run: python3 -I docs/build_cheatsheet.py
"""
import html
import pathlib
import re

here = pathlib.Path(__file__).resolve().parent
src = (here / "cheat-sheet.md").read_text(encoding="utf-8")


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    return s.replace("\\|", "|")


out, lines, i = [], src.splitlines(), 0
while i < len(lines):
    ln = lines[i]
    if ln.startswith("```"):
        j = i + 1
        while j < len(lines) and not lines[j].startswith("```"):
            j += 1
        out.append("<pre>" + html.escape("\n".join(lines[i + 1:j])) + "</pre>")
        i = j + 1
        continue
    if ln.startswith("|"):
        rows = []
        while i < len(lines) and lines[i].startswith("|"):
            cells = [c.strip() for c in re.split(r"(?<!\\)\|", lines[i].strip())[1:-1]]
            if not all(re.fullmatch(r":?-+:?", c) for c in cells):
                rows.append(cells)
            i += 1
        t = "<table><thead><tr>" + "".join("<th>%s</th>" % inline(c) for c in rows[0]) + "</tr></thead><tbody>"
        t += "".join("<tr>" + "".join("<td>%s</td>" % inline(c) for c in r) + "</tr>" for r in rows[1:])
        out.append(t + "</tbody></table>")
        continue
    m = re.match(r"(#{1,3}) (.*)", ln)
    if m:
        n = len(m.group(1))
        out.append("<h%d>%s</h%d>" % (n, inline(m.group(2)), n))
    elif ln.startswith("- "):
        items = []
        while i < len(lines) and lines[i].startswith("- "):
            items.append("<li>%s</li>" % inline(lines[i][2:]))
            i += 1
        out.append("<ul>" + "".join(items) + "</ul>")
        continue
    elif ln.strip():
        out.append("<p>%s</p>" % inline(ln))
    i += 1

page = """<!DOCTYPE html>
<html lang="de"><head><meta charset="UTF-8"><title>Spickzettel: Skizze → Wiener Melange</title>
<style>
@page{size:A4;margin:12mm}
*{box-sizing:border-box}
body{font:13px/1.45 "Lucida Sans Unicode","Lucida Grande",sans-serif;color:#292929;max-width:1100px;margin:0 auto;padding:24px}
h1{font-size:24px;margin:0 0 8px;border-bottom:4px solid #FF0000;padding-bottom:6px}
h2{font-size:17px;margin:18px 0 6px}
table{border-collapse:collapse;width:100%;margin:6px 0;break-inside:auto}
th,td{border-bottom:1px solid #D6D1CA;padding:3px 6px;text-align:left;vertical-align:top}
th{background:#F3F1EF}
code{background:#F3F1EF;padding:0 3px;font-size:12px;white-space:nowrap}
pre{background:#F3F1EF;padding:8px;font-size:11px;line-height:1.25;overflow:auto}
ul{margin:4px 0;padding-left:18px}
a{color:#1F4BAF}
</style></head><body>
""" + "\n".join(out) + "\n</body></html>\n"
(here / "cheat-sheet.html").write_text(page, encoding="utf-8")
print("wrote", here / "cheat-sheet.html")
