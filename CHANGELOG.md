# Changelog

## 0.1.0 — 2026-11-03

First version of the `wien-sketch-to-prototype` plugin (`/wien-revamp`) in the `stadt-wien-workflows` marketplace.

- A tagged Figma or Doop sketch becomes a clickable Doop prototype at 375 and 1440, built from Wiener Melange `<wm-*>` markup and theme v2.10.0. Copy comes only from the sketch.
- German cheat sheet and onboarding, Doop starter sketches, and a read-only Figma sketch reader.
- Pilot 1: sample sketch "Bäder in Wien" on the Doop starter canvas.
- Pilot 2: Figma sketch of wien.gv.at/freizeit/baden, compared with the live page.
- Install with the Claude marketplace, or with Vercel's skills CLI: `npx skills add dariob13/wien-sketch-to-prototype --skill wien-revamp`.
- `selfcheck.py` checks the tag vocabulary against the live handbook. A newsletter placed with a contact block uses the kontakt sample, opening hours and prices use "Tabelle in Card", and search follows the header template, `filter`, and `combobox`.
