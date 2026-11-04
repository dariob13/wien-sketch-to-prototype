# Icons and illustrations

**Hard rule:** every icon and every illustration that the workflow *chooses* comes from these two handbook pages, and from nowhere else:

- Icons (pictograms): <https://handbuch.wien.gv.at/look-and-feel/icons-und-illustrationen/icons/> (228 entries, cached in [icon-catalog.tsv](icon-catalog.tsv))
- Illustrations: <https://handbuch.wien.gv.at/look-and-feel/icons-und-illustrationen/illustrationen/> (219 entries, cached in [illustration-catalog.tsv](illustration-catalog.tsv))

Never use `search_icons`, other icon sets, emoji, generated images, stock art, or hand-drawn SVG instead. If nothing in the catalog fits, leave the icon out (or use the image placeholder for an illustration slot), and list it in the report as `Icon fehlt: <Begriff>` / `Illustration fehlt: <Begriff>`.

## Finding one

```bash
S=<skill dir>/scripts/fetch_assets.py
python3 -I $S icons telefon            # name, category, keywords → name, category, SVG URL
python3 -I $S illustrationen schwimm
python3 -I $S icons --all              # whole list
python3 -I $S --refresh                # rebuild the caches from the handbook (maintainers)
```

Search the German word first. Umlauts and ß are optional, and parts of words match (`schwimm` finds Schwimmbad). Pick the entry whose **name** matches the sketch's meaning. A keyword match alone is a weaker fit, so say which entry you picked in the report.

## Two kinds of icons: which rule applies

| Kind | Examples | Rule |
| --- | --- | --- |
| **UI icons that belong to a component** | Chevron in a back tag or CTA, burger/search/close in the header, download/external markers, accordion chevrons, social icons in the header menu or contact sample | Keep exactly the `<wm-icon iconid="…">` the fetched handbook sample has. They are part of the pattern's mechanics, not a design choice. Do not swap them for pictograms. |
| **Content icons the workflow chooses** | The big icon in "Teaser Card farbig mit Icon" or "Card responsive farbig mit Icon", icon rows in a card or list (`(Icon: …)` in the sketch), "Tag mit Icon", "Liste mit Icon und Link", any icon a sketcher asks for | **Only pictograms from the icon catalog.** |

Rule of thumb: if you would have to *decide which icon*, it is a content icon and comes from the catalog. If it arrived inside the sample and only its label changes, it is a UI icon. Leave it as is.

### Putting a pictogram into a component

The samples put content icons in `<wm-icon iconid="home" width="85">Text</wm-icon>`. `wm-icon` only knows its 79 built-in UI symbols and cannot load a file, so replace that one element with an `<img>` of the pictogram, keeping its place, size, and accessible text:

```html
<!-- Sample:  <wm-icon iconid="home" width="85">Linkt auf Seite</wm-icon> -->
<img src="https://handbuch.wien.gv.at/look-and-feel/icons-und-illustrationen/Markenmanagement/Piktogramme/SVG/SW_Piktogramme_Telefon.svg"
     width="85" height="85" alt="Linkt auf Seite">
```

- `width`/`height`: the sample's `width` (default 28 for icon rows when the sample gives none).
- `alt`: the wm-icon's text, if it had one. Use `alt=""` when the icon only decorates text next to it, for example in an icon row with the address beside it.
- Keep everything around it (slots, `wm-stack`, `wm-list`) unchanged.
- Add a source comment: `<!-- Icon: Telefon · https://handbuch.wien.gv.at/look-and-feel/icons-und-illustrationen/icons/ -->`.

The pictograms are black line art and are meant to be shown as they are. Do not recolor or crop them.

## Illustrations

- Use one only when the sketch asks for it: `[Illustration]`, `(Illustration: Schwimmbad)`, or `Illustration` written in an image box. A plain `(Bild)` or X box is a photo slot and stays the grey image placeholder. Do not replace photos with illustrations on your own.
- Pick from the illustration catalog by name or keyword. Embed as `<img src="<catalog URL>" alt="<sketch label or name>">` in the slot where the sample has its image (`slot="media"` etc.).
- **The handbook requires sign-off:** "Wenn Sie eine Illustration verwenden möchten, stimmen Sie sich bitte mit dem Handbuch-Team ab." Every illustration used goes on the report's open-items list as `Illustration „<Name>“ – Freigabe Handbuch-Team nötig`.
- No match: grey image placeholder plus `Illustration fehlt: <Begriff>` in the report.

## In the report

Add a line per page when icons or illustrations were placed:

```
**Icons:** Karte 2 → Piktogramm „Telefon“ · Liste Zeile 1 → „Standortzeichen“ · `(Icon: Rakete)` → kein Treffer, weggelassen
**Illustrationen:** Bühne → „Schwimmbad“ (Freigabe Handbuch-Team nötig)
```
