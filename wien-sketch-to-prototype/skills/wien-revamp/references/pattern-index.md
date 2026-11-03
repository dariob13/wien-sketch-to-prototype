# Pattern index

67 pattern pages on <https://handbuch.wien.gv.at/pattern-library/patterns/>, listed 2026-11-03. The handbook page is the catalog that counts. If a slug 404s, open the index and follow the current link. Do not guess a component name that is not on that page.

Fetch before use. This table is only the address book. It does not document slots or attributes.

## Layout

| Pattern | Slug |
| --- | --- |
| Header | `header` |
| Stage | `stage` |
| Section | `section` |
| Stack | `stack` |
| Grid | `grid` |
| Footer | `footer` |
| Trenner | `divider` |

## Navigation and actions

| Pattern | Slug |
| --- | --- |
| Menü | `menu` |
| Suche | `suche` |
| Sidebar | `sidebar` |
| In-Page Navigation | `in-page-navigation` |
| Anker | `anker` |
| Skip Link | `skip-link` |
| Links | `links` |
| Hervorgehobener Link | `hervorgehobener-link` |
| Quicklink-Liste | `quicklink-liste` |
| Reiter | `reiter` |
| Paginierung | `paginierung` |
| Pager | `pager` |
| Button | `button` |
| Tag | `tag` |

`suche` has no Vorschau samples. A search field in the header is the header template. A filter or a combobox search is `filter` or `combobox`. `fetch_pattern.py suche` follows those links. See tag-vocabulary.md.

## Content

| Pattern | Slug |
| --- | --- |
| Card | `card` |
| Karussell | `karussell` |
| Liste | `liste` |
| Tabelle | `tabelle` |
| Akkordeon | `akkordeon` |
| Details | `details` |
| Vorspann | `vorspann` |
| Exposé | `expose` |
| Hervorhebung | `hervorhebung` |
| Infobox | `infobox` |
| Meldung | `meldung` |
| Zitat | `zitat` |
| Kontakt | `kontakt` |
| Newsletter | `newsletter` |
| Zeitstempel | `zeitstempel` |
| Status | `status` |
| Chip | `chip` |
| Modal | `modal` |
| Flip-Card | `flipcard` |
| Breaking News | `breakingnews` |

## Media

| Pattern | Slug |
| --- | --- |
| Bild | `bild` |
| Copyright | `copyright` |
| Galerie | `galerie` |
| Video-Player | `video` |
| Audio-Player | `audio` |
| Map | `map` |
| Icon | `icon` |
| Logo | `logo` |

## Forms

| Pattern | Slug |
| --- | --- |
| Formular: Block | `formular-block` |
| Formular: Layouts | `formular-layouts` |
| Formular: Validierung | `formulare` |
| Formular: Input | `input` |
| Formular: Textfeld | `textfeld` |
| Formular: Checkbox | `checkbox` |
| Formular: Radio | `radio` |
| Formular: Select | `select` |
| Formular: Combobox | `combobox` |
| Formular: Switch | `switch` |
| Formular: Filter | `filter` |
| Formular: Upload | `upload` |
| Formular: Fehlerliste | `fehlerliste` |
| Formular: Fortschrittsanzeige | `fortschrittsanzeige` |
| One Time Password | `OneTimePassword/otp` |

## Other

| Pattern | Slug |
| --- | --- |
| Bot | `bot` |
| Fetch | `fetch` |
| Social Media | `social-media` |

Full URL: `https://handbuch.wien.gv.at/pattern-library/patterns/<slug>/`

## Regions that show up on almost every wien.gv.at page

Fetch these by default, then add only the patterns the brief and the live page need:

1. `header` — the wien.gv.at variant (logo, search, menu), not the microsite sample.
2. `stage` — the variant that matches the live page (image and title, image and title and CTA, or title only).
3. `section`, `stack`, `grid` — as the live page groups content.
4. `footer` — the legal link list and the copyright line. Keep the official link names.

Cards, tags, quicklinks, and contact are common next, and they are still separate fetches (`card`, `tag`, `quicklink-liste`, `kontakt`).
