# Fetching pattern HTML

The pattern library is the source of the markup. A remembered snippet is not.

## Use the script

`scripts/fetch_pattern.py` does the steps below for you. It uses the standard library only.

```bash
S=<skill dir>/scripts/fetch_pattern.py
python3 -I $S --version                       # theme version for page-shell.md
python3 -I $S card --list                     # variant names with index
python3 -I $S card --variant "farbig mit Text"
python3 -I $S stage --index 0                 # the unheaded default sample
```

Add `--compact` to collapse whitespace; for the header it also drops the nested demo submenus (use it for the header, always). A trailing `(Standard – ohne Überschrift)` entry after the named variants is usually a demo inside the property table, so ignore it.

It prints each sample with a `<!-- Source: … — variant n: … -->` line, makes `/images/...` URLs absolute, and replaces "… öffnen" template links (the header) with the real element. Fetch several patterns in one shell call when you can. If the script fails (network, changed page structure), do the manual steps below and mention it in the handoff.

## Manual steps

Index: <https://handbuch.wien.gv.at/pattern-library/patterns/>

Pattern URL: `https://handbuch.wien.gv.at/pattern-library/patterns/<slug>/`

Slugs are in [pattern-index.md](pattern-index.md). Fetch the **raw HTML** of the pattern page (curl or a browser). A markdown conversion of the page drops the attributes and slots you need.

## Where the example sits

Each variant is a heading followed by a tab pair.

- The variant name is the `h3` in the `wm-anchor` just above the sample.
- The copyable markup is the inner HTML of `wm-tabpanel.code-preview-rendered` (the tab labelled **Vorschau**). It is real markup, not escaped.
- `pre.language-html` (the tab labelled **Code**) is the same example run through a syntax highlighter: token spans and `&lt;` entities. Use it only if the Vorschau panel is missing, and strip the spans and decode the entities first.

**Exception: the header.** On `/patterns/header/`, every Vorschau panel holds only a `wm-cta` link "Header … öffnen" pointing to a template page. Copying that panel would give you a link instead of a header. Fetch the template page it links to and copy its `<wm-header>…</wm-header>` element whole, including the logo SVG:

- wien.gv.at header: `https://handbuch.wien.gv.at/pattern-library/templates/patterns/header/standard/`
- English: `…/templates/patterns/header/standard-englisch/`

Its menu links are `#` placeholders. Keep the labels, which are official navigation, and leave the `#` links as they are. Do this for any pattern whose Vorschau panel is only an "… öffnen" link (checked 2026-11-03).

Skip the handbook chrome. The page has its own `wm-header`, a title `wm-stage` named after the pattern ("Stage", "Card", …), and a sidebar `Alle Patterns`. Those are not the examples. Examples live under `.pl-samples`.

## What to keep

- The tags, including every `<wm-*>`, and the text inside them.
- Slot names (`slot="content"`, `slot="heading"`, `slot="media"`, `slot="postcontent"`, …).
- Attributes on the example (`size`, `color`, `gap`, `clickable`, `kind`, `type`, `iconid`, …). Copy the ones the variant uses. Do not add attributes you did not see on that example or on the pattern's property table.
- The logo `<svg>` inside the header example. Copy the paths. Do not redraw the shield.
- A source comment above the region:

```html
<!-- Source: https://handbuch.wien.gv.at/pattern-library/patterns/card/ — variant: Teaser -->
```

## What to change

- Visible German (or the live page's) wording, `href`s, and image URLs, so the example's demo content ("Gemeinderatswahl 2025", "Lorem ipsum", `#`) does not ship.
- Image `src` values that start with `/` — make them absolute, as [page-shell.md](page-shell.md) says.
- Nothing else. If the live page needs a region the pattern cannot express, fetch the closest pattern, keep it intact, and note the gap in the handoff.

Fetch a pattern once per task even if this skill mentions it. The handbook example wins over any template cached in an older skill or in the conversation.
