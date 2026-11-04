# Tag vocabulary

This file is the single source of truth for turning sketch tags into Wiener Melange patterns. `docs/cheat-sheet.md` is the short human version of it. When you change one, change the other.

Pattern slugs are pages under `https://handbuch.wien.gv.at/pattern-library/patterns/<slug>/`. Variant names are the `h3` headings above a Vorschau panel on that page, checked on 2026-11-03 (theme v2.10.0). Always fetch the page before building. If a variant name has changed, use the closest current one and note it in the report. A page with no Vorschau panels (currently `suche`) is not a source of markup: the row names the patterns that are.

## How a tag is read

A **box** is any rectangle, frame, group, or element in the sketch. Its **tag** says which pattern it becomes, and its **text** is the content.

1. **Bracketed text in the box:** `[Bühne]`, `[cards x3]`. This is the normal form.
2. **Layer name:** `[Bühne]`, or a plain non-default name such as `Bühne` or `Quicklinks`. Default names (`Rectangle 12`, `Frame 3`, `div`) are not tags.
3. **Bare pattern word:** a box whose only text is a known tag word (`Header`, `Footer`, `Karussell`). It counts as a tag, not as content. Mention that you read it this way.
4. **Inherited:** a tag on one box of a row or column of look-alike boxes (same size within ~10 %, same structure) applies to the untagged siblings. A tag on the box that frames a group (`[Kacheln x3]` around three boxes) applies to the boxes inside it. Report inherited tags as `Tag ✓`.
5. **No tag:** guess from shape and position (see [sketch-reading.md](sketch-reading.md) → Untagged boxes) and mark the result as a guess.

Matching is forgiving:

- Case does not matter. Umlauts are optional (`Buehne`, `Buhne`, `Bühne`), and so are hyphens and spaces (`Quick-Links`, `quick links`).
- Singular and plural both work (`Karte`/`Karten`, `card`/`cards`). German and English can be mixed freely.
- Obvious typos within one or two letters of a known word work too (`Karusell`, `Akordeon`). Report the correction.
- A word that is not in this file is an **unknown tag**. Do not invent a pattern for it. Use the closest entry only if it is clearly what was meant (`[Teaserbox]` → card); otherwise ask.

### Modifiers

Modifiers follow the tag word inside the same brackets, in any order: `[Karten x3 mit Bild]`, `[section grey]`.

| Modifier | Also understood | Effect |
| --- | --- | --- |
| Count | `x3`, `3x`, `3 Spalten`, `3 cols`, `3 columns`, `3er` | Number of items, and the column count on desktop (max. 4; more items wrap into rows) |
| Highlighted | `grau`, `hinterlegt`, `Hintergrund`, `grey`, `gray`, `highlight`, `bg` | Section with background (Nebelgrau band) |
| With image | `mit Bild`, `Bild`, `Foto`, `with image`, `img` | Image variant |
| No image | `ohne Bild`, `no image`, `text only`, `nur Text` | Text variant |
| Title only | `nur Titel`, `title only`, `ohne Text` | Title-only variant |
| Colored | `farbig`, `Farbe`, `colored`, `colour` | Colored variant (Teaser Card farbig, Stage mit Farbe) |
| Light color | `hell`, `light` | Stage mit Light-Farbe |
| Small / large | `klein`, `small` / `groß`, `gross`, `large`, `big` | Small or large variant where one exists |
| Full width | `volle Breite`, `breit`, `full`, `full width`, `100%` | Full-width variant |
| Color name | `goldgelb`/`gelb`/`yellow`, `frischgrün`/`grün`/`green`, `wasserblau`/`blau`/`blue`, `nebelgrau`/`grau`/`grey`, `Rahmen`/`border` | Color variant for Hervorhebung and button groups only. Never invent a color for a pattern that has no color variant. |
| Link target | `→ Seitenname`, `-> Seitenname`, `link: Seitenname`, `→ https://…` | Click-through target. See sketch-reading.md → Links. |

### Special tags

| Tag | Also understood | Meaning |
| --- | --- | --- |
| `[Notiz]` | `[Note]`, `[Kommentar]`, `[ignore]`, `[ignorieren]`, `[todo]`, lines starting with `//` | An instruction from the sketcher to you. Follow it, but do not build it. |
| `[?]` | `[??]`, `[egal]`, `[AI]`, `[vorschlagen]`, `[suggest]` | "I don't know which pattern, you choose." Choose, and mark it as a guess. |
| `[aus]` | `[hidden]`, `[off]`, `[skip]` | Skip this box completely. |

## How box text becomes content

The sketch's text is the only copy that ships. **Never write new copy, and never keep handbook demo text** ("Gemeinderatswahl 2025", "Lorem ipsum", "Alsergrunder Kultursommer").

| In the box | Becomes |
| --- | --- |
| First line, or the largest/boldest text | Heading of the pattern (H1 in the stage, H2 in sections and cards) |
| Following lines | Body text |
| Lines starting with `-`, `•`, `*`, `1.` | List items or links, depending on the pattern |
| `Text →`, `Text >`, `> Text`, `Text ›`, or underlined text | Link or CTA label |
| `(Bild)`, `[Bild]`, a box with an X through it, a picture fill, or an image | Image slot (see below) |
| `Bild: https://…` | That image URL, used as is |
| `(Icon: Telefon)` | A pictogram from the handbook icon page, found with `scripts/fetch_assets.py icons telefon` and embedded as `<img>` in the sample's icon slot (see [icons-illustrations.md](icons-illustrations.md)). No match → no icon, reported. |
| `(Illustration: Schwimmbad)` | An illustration from the handbook illustration page (`fetch_assets.py illustrationen schwimm`) in the image slot. Needs sign-off from the Handbuch team, so report it. |
| Nothing | `[Text fehlt]` in the slot, and the box goes on the report's "Text fehlt" list |

**Required versus optional parts of a sample.** A sample's *required* slots (the heading of a stage, card, or section, the label of a link or button, the items of a list) are filled from the sketch, or else get a placeholder. Its *optional extras* are **dropped** when the sketch does not ask for them: a CTA in the stage, social icons and the newsletter card in the contact sample, an extra card, a chip, a category label. Do not fill an optional extra with demo content or a placeholder. Mention each one you dropped in the report only if it changes how the page looks (for example "Kontakt-Sample ohne Newsletter-Karte").

**Text with no slot.** If the sketch has text the chosen sample has no slot for, do not drop it. Example: a subtitle under the stage H1 (the stage only takes H1 and CTA). Put it into the nearest pattern that holds it: a stage subtitle becomes the `wm-teaser-text` paragraph of a Vorspann right after the stage, or goes in front of the existing Vorspann's text. Report where it went.

Missing content stays visible as a bracketed placeholder in German: `[Text fehlt]`, `[Überschrift fehlt]`, `[Link-Ziel fehlt]`, `[Bild fehlt]`. Keep the sketcher's wording exactly, including their spelling. List obvious typos in the report, but do not fix them.

**Page chrome is not sketch copy.** Header and footer keep the official labels from the handbook example (menu, search, legal links, copyright). They are official Stadt Wien chrome, not invented text.

**Images.** An image slot with no permitted image becomes the theme's Nebelgrau-light placeholder (`#F3F1EF`) with an `alt` built from the sketch label, or `[Bild]`. Do not use stock photos, generated images, or handbook demo photos.

## Page chrome

Header and footer appear on every wien.gv.at page. **Add them even when the sketch leaves them out**, and say so in the report. Leave them out only if the sketcher writes `[ohne Header]` / `[ohne Footer]` (or `[no header]` / `[no footer]`).

| Tag | Also understood | Pattern (slug) | Variant |
| --- | --- | --- | --- |
| Header | Kopfzeile, Kopf, Kopfbereich, Navigation, Nav, Navbar, Menüleiste, Top bar | `header` | The wien.gv.at header (first sample: logo, search, menu). `englisch`/`english` → "Header wien.gv.at English". Never use the Sonderauftritte variants unless the sketch says `Sonderauftritt`/`Microsite`. |
| Footer | Fußzeile, Fusszeile, Fuß, Fuss, Seitenende, Bottom | `footer` | The only sample |

## Top of the page

| Tag | Also understood | Pattern (slug) | Modifier → variant | Sketch text → slots |
| --- | --- | --- | --- | --- |
| Bühne | Stage, Hero, Aufmacher, Titelbild, Kopfbild, Headerbild, Titel, Seitentitel | `stage` | image or `mit Bild` → "Stage mit Headerbild, Titel und hervorgehobenem Link" · `nur Titel` → title-only stage (handbook default sample) · `farbig` → "Stage mit Farbe" · `hell`/`light` → "Stage mit Light-Farbe" · `Video` → "Stage mit Video" · `Karussell`/`Slider` → "Stage mit Karussell" | 1st line → H1; `Text →` → highlighted link (`wm-cta`; drop the CTA if there is none); further lines have no stage slot → Vorspann (see "Text with no slot") |
| Tags | Tag-Liste, Schlagworte, Schlagwörter, Themen, Filter-Tags, Pills | `tag` | above the stage in the sketch → "Tags über Stage" · below the stage → "Tags unter der Stage" · many tags (more than about 6) → "Tag-Liste mit Scrollbalken" · otherwise "Tag-Liste" | One tag per line or per pill. `← Text`, `< Text`, `zurück: Text` → parent-channel tag ("Tag mit Navigationsfunktion", chevron-left). `(Icon: …)` → "Tag mit Icon". |
| Vorspann | Intro, Einleitung, Lead, Lead-Text, Teaser-Text, Einführung | `vorspann` | — | All text → lead paragraph |
| Inhalt | Inhaltsverzeichnis, Sprungnavigation, Sprungmarken, In-Page-Navigation, Seitennavigation, TOC, Table of contents | `in-page-navigation` | `Dropdown` → "In-Page Navigation mit Dropdown" · otherwise "In-Page Navigation mit Scrollbalken" | Lines → jump links (they must match H2s on the same page; report any that don't) |
| Meldung | Hinweis, Warnung, Fehler, Erfolg, Notice, Alert, Banner, Info-Banner, Warning | `meldung` | `Warnung`/`warning` → "Warnung" · `Fehler`/`error` → "Fehlermeldung" · `Erfolg`/`success` → "Erfolgsmeldung" · `Hinweis`/`info` → "Hinweis - wegklickbar" · add `wegklickbar`/`schließbar`/`dismissible` → the "- wegklickbar" version | All text → message |

## Layout

| Tag | Also understood | Pattern (slug) | Modifier → variant | Notes |
| --- | --- | --- | --- | --- |
| Abschnitt | Section, Bereich, Block, Sektion, Band | `section` | `grau`/`highlight`/… → "Section mit Hintergrund" with `highlight="nebelgrau"`. Other colors map to the property values `goldgelb`, `frischgruen`, `wasserblau`, `morgenrot`, `flieder`, `abendstimmung` (`gelb` → goldgelb, `grün` → frischgruen, `blau` → wasserblau, `rot` → morgenrot, `lila` → flieder) | A box that contains other boxes. 1st line (if it is not inside a child box) → section H2. Cards inside a highlighted section have no shadow. |
| Raster | Grid, Spalten, Columns, Reihe, Row | `grid` | `wm-grid` has no column attribute. Its `size` sets the card width: 2 columns → `size="l"`, 3 → `size="m"`, 4 → `size="s"` (cards in a 4-grid also get `size="s"`), 1 → `size="full"` | Usually implied: three equal boxes side by side need no `[Raster]`. Build a grid automatically for repeated items. |
| Stapel | Stack, untereinander, vertikal | `stack` | `viel Abstand` → "Stack mit viel Abstand" · `volle Breite` → "Stack volle Breite" | Mostly implied. Use it when the sketch stacks unrelated items with even gaps. |
| Trenner | Trennlinie, Linie, Divider, Line, hr, Separator | `divider` | `zentriert`/`centered` → "Trenner zentriert" | A thin full-width line between sections, even untagged |

## Cards and boxes

> **"Karte" is ambiguous in German**: it can mean a card or a map. Treat `[Karte]` as a **map** when the box mentions Stadtplan, Standort, Adresse, Lage, a pin, or shows a map-like picture; otherwise treat it as a **card**. Report which reading you chose. The cheat sheet tells people to write `Kachel`/`Card` or `Stadtplan`/`Map` to avoid this.

| Tag | Also understood | Pattern (slug) | Modifier → variant | Sketch text → slots |
| --- | --- | --- | --- | --- |
| Kachel | Card, Cards, Karte (see note), Karten, Kacheln, Teaser, Teaser-Box, Box, Tile | `card` | image → the first, unheaded sample on the card page (teaser card: `size="m" clickable`, heading, image, text); with a short label above the title → "Teaser Card mit Kategorie"; with icon rows (`(Icon: pin) Adresse`) → "Teaser Card mit Icon-Zeilen" · `farbig` → "Teaser Card farbig mit Text" (with an icon → "Teaser Card farbig mit Icon") · `nur Titel` → "Teaser Card ohne Text" · no image, heading + text → "Card mit Überschrift und Text" · plus a link line → "Card mit Überschrift, Text und Link" · plus a button → "Card mit Text und Button" · `volle Breite` → "Card volle Textbreite" (with image → "Card responsive mit Bild") · `Links`/list of links → "Card mit Links und Bild" / "Card mit Links ohne Bild" · `Quicklinks` inside → "Card mit Quicklink-Liste" · `Tabelle` inside → "Card mit Tabelle" · `Tags` inside → "Card mit Tags" · `Visitenkarte`/`Person` → "Card Visitenkarte 50 Prozent" (`volle Breite` → "… 100 Prozent") · `Störer`/`Badge` → "Card mit Störer eckig" (`rund` → "… rund") · `Video` → "Card mit Video" | Small label above the title → category; 1st line → H2/H3 title; next lines → text; `Text →` → link; `→ Seite` → whole card links there |
| Karten-Reihe | Card row, Reihe Karten | `card` | `klein` → "Reihen mit kleinen Teaser Cards" · `groß` → "Reihen mit großen Teaser Cards" · otherwise "Reihen mit mittleren Teaser Cards" | Used automatically when 3–4 equal image cards sit in a row |
| Karussell | Carousel, Slider, Swiper, Galerie-Slider, Teaser-Slider | `karussell` | `klein` → "Karussell mit kleinen Cards" · otherwise "Karussell mit großen Cards" | Each child box → one card (same rules as Kachel). Fewer than 3 children → report it; a carousel of 1–2 cards is not a carousel. |
| Infobox | Info-Box, Steckbrief, Fakten, Factbox, Auf einen Blick | `infobox` | `Galerie` → "Horizontale Infobox mit Galerie" · `Video` → "Horizontale Infobox mit Video" · `Stadtplan`/`Map` → "Vertikale Infobox mit Map" · `Visitenkarte` → "Horizontale Visitenkarte" (`vertikal` → "Vertikale Visitenkarte") · image → "Infobox als Card responsive mit Bild" · `farbig` → "Infobox als Card responsive farbig mit Icon" | `Label: Wert` lines → info rows |
| Exposé | Expose, Projekt-Steckbrief, Vorstellung | `expose` | — | Heading, text, image, link |
| Hervorhebung | Highlight-Box, Kasten, Merkkasten, Wichtig, Callout, Infokasten | `hervorhebung` | `gelb` → "Hervorhebung mit Hintergrundfarbe - Goldgelb" · `grün` → "… - Frischgrün" · `blau` → "… - Wasserblau" · `grau` → "… - Nebelgrau" · `Rahmen`/`border` → "Hervorhebung mit Rahmenlinien - Fast Schwarz" · no color → Nebelgrau | Heading and text. **English `[highlight]` alone:** on a full-width box that contains other boxes → highlighted section (Abschnitt grau); on a small box with text → Hervorhebung. |
| Zitat | Quote, Statement, Aussage | `zitat` | `großes Bild` → "Zitat mit großem Bild" · otherwise "Zitat mit Bild" | Quote text; `— Name` → author |
| Kontakt | Contact, Ansprechperson, Ansprechpartner, Kontaktbox | `kontakt` | `Details` → "Kontakt mit Details" · `Infobox` → "Kontakt in Infobox" · inside the page body → "Kontakt innerhalb der Seite" · `Stadtservice` → "Kontakt Stadtservice" · otherwise the page-end contact | Name, department, phone, email, address **only from the sketch**. Missing → `[Telefonnummer fehlt]` etc. Never invent contact data. |
| Newsletter | Newsletter-Anmeldung, Abo | `newsletter` | `Kontakt` in the same box or beside it → the default sample of `kontakt` (contact card plus newsletter card) · otherwise "Newsletter Section". The newsletter page has no Kontakt variant. | Heading, text, button label |
| Chip | Status-Chip, Label, Badge (outside a card) | `chip` | `positiv`/`ja`/`offen` → "Chip positiv" · `negativ`/`nein`/`geschlossen` → "Chip negativ" · `klein`/`groß` → size | Text → chip label |
| Zeitstempel | Zuletzt geändert, Stand, Aktualisiert, Datum, Timestamp, Last updated | `zeitstempel` | `Details` → "Zeitstempel mit Detailinfos" · otherwise "Zeitstempel \"Zuletzt geändert\"" | Date from the sketch only. Missing → `[Datum fehlt]` |

## Lists and links

| Tag | Also understood | Pattern (slug) | Modifier → variant | Sketch text → slots |
| --- | --- | --- | --- | --- |
| Quicklinks | Quicklink-Liste, Quick-Links, Schnellzugriff, Wichtige Links, Top-Links, Pfeil-Links | `quicklink-liste` | `3 Spalten` → "Quicklink-Liste - 3 Spalten" · otherwise "Quicklink-Liste - 2 Spalten" · inside a grey section → "Quicklink-Liste auf Section mit Hintergrundfarbe" · `Chip` → "Quicklink-Liste mit Chip" | One link per line; `→ Seite` per line works |
| Liste | List, Aufzählung, Bullets, Punkte, Stichpunkte | `liste` | `nummeriert`/`1.`/`numbered` → "Liste mit Aufzählung (ordered List)" · lines are links → "Liste mit Links" · `Trennstrich`/`divider` → "Liste mit Trennstrich ohne Links" (with links → "… und Link", with images → "Liste mit Trennstrich sowie Bild und Link") · `Icon` → "Liste mit Icon und Link" | One item per line |
| Termine | Veranstaltungen, Events, Event-Feed, Kalender-Liste | `liste` | `Bild` → "Event-Feed mit Bildern" · `Details` → "Event-Feed mit Details" · otherwise "Event-Feed" | Date, title, place per item, only from the sketch |
| Linkliste | Links, Weiterführende Links, Mehr zum Thema, Related links | `liste` | → "Liste mit Links" | One link per line |
| Download | PDF, Datei, Dokument, File | `links` | → "Download Link" | Label; file type and size only if written |
| Extern | Externer Link, External link | `links` | → "Externer Link" | Label and URL |
| Mehr-Link | CTA, Weiterlesen, Mehr, Alle anzeigen, Pfeil-Link, Call to action, More | `hervorgehobener-link` | `rechts`/`right` → "Hervorgehobener Link rechtsbündig über ganze Breite" · `Button` → "Hervorgehobener Link als Button" · `zurück`/`back` → "Hervorgehobener Link Pfeil umgedreht" · otherwise "Hervorgehobener Link" | Label; `→ Seite` → target |
| Button | Knopf, Schaltfläche, Btn | `button` | `sekundär`/`secondary` → "Button sekundär" · `tertiär`/`tertiary`/`Textbutton` → "Button tertiär" · `Icon` → the "… mit Icon" version · `klein` → "Button sekundär klein" · several buttons in a row → "Button-Gruppe" · otherwise primary (`Button Call-to-Action` if it is the main action) | Label; `→ Seite` → target |
| Reiter | Tabs, Registerkarten, Tab-Leiste | `reiter` | — | Tab labels on the first line or as child boxes; the content per tab comes from child boxes |
| Akkordeon | Accordion, Aufklapper, Ausklappliste, FAQ, Fragen, Klappbox | `akkordeon` | `offen`/`open` → "Akkordeon alle Elemente geöffnet" · `eins offen` → "Akkordeon mit einzelnem Element geöffnet" · `Icons` → "Akkordeon alle Elemente geschlossen mit Icons" · otherwise all closed | `+ Frage` / `▸ Frage` lines → item headings; the text under each → its content |
| Details | Mehr anzeigen, Aufklapptext, Weitere Infos (aufklappbar), Expand | `details` | — | Summary line, then hidden text |
| Tabelle | Table, Öffnungszeiten, Preise, Preisliste, Tarife | `tabelle` | `Öffnungszeiten`, `Preise` or `Tarife` inside a card → "Tabelle in Card" (those words are h3 headings inside that sample, not variants) · the same tags on a plain table → the default table · `ohne Rahmen` → "Tabelle ohne Rahmen" · `komplex` → "Tabelle komplex" · `sortierbar` → "Tabelle sortierbar" · `ViennaViz` → "Tabelle ViennaViz" · otherwise the default table | Rows from lines; columns split on `\|`, a tab, or two or more spaces. **Prices and hours only from the sketch.** |
| Seiten | Paginierung, Pagination, Blättern, Seitenzahlen, 1 2 3 … | `paginierung` | → "Paginierung automatisch mit Cards" when it follows cards, otherwise a manual pagination sample | Page numbers are illustrative; say so in the report |
| Pager | Vor/Zurück, Weiter/Zurück, Prev/Next | `pager` | — | Two labels; `→ Seite` → targets |
| Suche | Suchfeld, Search, Suchbox, Suchergebnisse | `suche` · `header` · `filter` · `combobox` | The suche page has no Vorschau samples. `fetch_pattern.py suche` follows the links on that page. A search field in the header, or `[Suche]` with no modifier, only confirms the header: use the wien.gv.at header template `/pattern-library/templates/patterns/header/standard/`. `Filter` → the default sample of `filter`. `Vorschläge` or `Combobox` → the default sample of `combobox`. `Ergebnisse` or `results` → cards from the sketch (`card`); the page has no result sample. | Placeholder text, results from the sketch. |

## Media

| Tag | Also understood | Pattern (slug) | Modifier → variant | Notes |
| --- | --- | --- | --- | --- |
| Bild | Foto, Image, Img, Picture, Grafik, a box with an X | `bild` | `Beschreibung`/`caption` text under it → "Bild mit Beschreibung" · `Quelle`/`©` → "Bild mit Quelle" · `Lightbox`/`groß öffnen` → "Bild mit Modal (Lightbox)" · otherwise "Bild mit Beschreibung" without caption | Placeholder image unless a URL is given |
| Galerie | Gallery, Bilder, Fotos, Bildergalerie | `galerie` | → "Galerie mit kleinen Vorschaubildern" | Each image child is one image |
| Video | Film, Clip, YouTube, Player | `video` | `in Card` → "Video-Player in Card" · `Transkript` → "Video-Player in Card mit Transkript" · `Livestream`/`live` → "Video-Player in Card mit Livestream" · otherwise "Video-Player eingebettet mit Beschreibung" | Video URL only if written; otherwise an empty player and `[Video fehlt]` |
| Audio | Podcast, Hörbeitrag | `audio` | `Transkript` → "Audio-Player in Card mit Transkript zum Aufklappen" · `Podcast` → "Audio-Player Podcast Widget" · otherwise "Audio-Player in Card mit Transkript-Link" | Title from the sketch |
| Stadtplan | Map, Lageplan, Standort, Landkarte, Karte (see note above), Plan | `map` | — | A labelled map placeholder, as in the Doop prototyper rules. Do not draw a fake map. Pins/addresses only from the sketch. |
| Icon | Symbol, Piktogramm | `icon` | — | Only inside other patterns. **Only pictograms from <https://handbuch.wien.gv.at/look-and-feel/icons-und-illustrationen/icons/>** (catalog + `fetch_assets.py icons <Wort>`). The `wm-icon` UI symbols that come inside a sample stay as they are. See icons-illustrations.md. |
| Illustration | Zeichnung, Grafik (illustriert), Illu | `bild` | — | **Only illustrations from <https://handbuch.wien.gv.at/look-and-feel/icons-und-illustrationen/illustrationen/>** (`fetch_assets.py illustrationen <Wort>`), in the image slot of the surrounding pattern. Each one needs Handbuch-team sign-off, so report it. No match → image placeholder. |
| Social Media | Teilen, Share, Folgen, Social | `social-media` | `Facebook` / `LinkedIn` / `YouTube` / `X`/`Twitter` → that sample · inside an infobox → "Infobox mit Social Media" | — |

## Not in version 1

These tags are understood, but they are **not built** in v1. Leave a labelled gap that names the tag and says it is planned for a later version, and list it in the report:

- Forms: `Formular`, `Form`, `Eingabefeld`, `Input`, `Textfeld`, `Checkbox`, `Radio`, `Auswahl`/`Select`, `Dropdown` (as a form field), `Upload`, `Schritte`/`Fortschritt`/`Stepper`, `Login`, `OTP`
- Special sites and app chrome: `Sidebar`, `Sonderauftritt`, `Breaking News`, `Bot`/`Chatbot`, `Status` (Regierungsmonitor), `Flip-Card`, `Modal`/`Dialog` (as a page element)

A labelled gap looks like this (theme colors, no invented component):

```html
<!-- Gap: [Formular] is not supported in v1 -->
<wm-section><div style="border:2px dashed #292929;padding:20px">[Formular – in Version 1 noch nicht unterstützt]</div></wm-section>
```
