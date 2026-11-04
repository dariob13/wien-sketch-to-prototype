# Changelog

## 0.3.0 — 2026-11-04

- No terminal needed. `dist/wien-revamp.zip` uploads in the Claude app (Customize > Skills > Upload a skill), or a Team/Enterprise owner provisions it for everyone. Doop and Figma connect as connectors in the app. Build the ZIP with `tools/build-zips.sh`.
- Offline handbook snapshot in `references/samples/` (52 patterns, theme v2.10.0), made with `scripts/snapshot_patterns.py`. The skill uses it when its sandbox cannot reach handbuch.wien.gv.at. `selfcheck.py` checks that its theme version is current.
- Handbook changes from 2026-11-04: `divider` is now `trenner`, there is a new pattern `ladebildschirm`, and the icon catalog (227) and illustration catalog (207) are refreshed.
- References to `AskUserQuestion` and `figma-use` now work in clients that lack them.
- German guides in `guides/` describe the setup in the app only.

## 0.2.0 — 2026-11-04

- Icons and illustrations: only the official handbook sources are allowed. Icons come from <https://handbuch.wien.gv.at/look-and-feel/icons-und-illustrationen/icons/> (228 pictograms) and illustrations from <https://handbuch.wien.gv.at/look-and-feel/icons-und-illustrationen/illustrationen/> (219). New `scripts/fetch_assets.py` (catalog and search, `--refresh`) and `references/icons-illustrations.md` (rules and embedding). Cached catalogs are in `references/*-catalog.tsv`.
- UI icons that come inside a component sample stay as `wm-icon`. Content icons are pictogram `<img>`s in the sample's icon slot (tested with the real theme: farbige Teaser-Card, Icon-Zeilen, Tag, Illustration im Bild-Slot).
- Illustrations are marked in the report as needing sign-off from the Handbuch team (the handbook's own rule).
- New tag `[Illustration]`, and the sketch syntax `(Icon: Telefon)` / `(Illustration: Schwimmbad)`. Both are in the cheat sheet.
- `selfcheck.py` also checks that both catalogs match the handbook.

## 0.1.0 — 2026-11-03

First version of the `wien-sketch-to-prototype` plugin (`/wien-revamp`) in the `stadt-wien-workflows` marketplace.

- A tagged Figma or Doop sketch becomes a clickable Doop prototype at 375 and 1440, built from Wiener Melange `<wm-*>` markup and theme v2.10.0. Copy comes only from the sketch.
- German cheat sheet and onboarding, Doop starter sketches, and a read-only Figma sketch reader.
- Pilot 1: sample sketch "Bäder in Wien" on the Doop starter canvas.
- Pilot 2: Figma sketch of wien.gv.at/freizeit/baden, compared with the live page.
- Install with the Claude marketplace, or with Vercel's skills CLI: `npx skills add dariob13/wien-sketch-to-prototype --skill wien-revamp`.
- `selfcheck.py` checks the tag vocabulary against the live handbook. A newsletter placed with a contact block uses the kontakt sample, opening hours and prices use "Tabelle in Card", and search follows the header template, `filter`, and `combobox`.
