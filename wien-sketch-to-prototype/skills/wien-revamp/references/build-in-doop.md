# Building in Doop

Doop is the only output. Every frame is one HTML document that loads the official theme CSS and `bundle.min.js`, so the `<wm-*>` components render for real. Adapted from the `stadt-wien-doop-prototyper` workflow.

Use one `agent_name` for the whole task: `Wien Revamp`.

## Where the prototype goes

| Sketch in | Prototype goes to |
| --- | --- |
| Doop | The **same canvas**, on a page named `Prototyp` (add it with `set_canvas_pages` and keep the existing pages; pass the old list as `expectedPages` if asked). |
| Figma | A **new canvas** `Stadt Wien Entwurf - <Topic>` (topic = the sketch page or file name, plain hyphen with spaces). Pages: `Skizze` and `Prototyp`. On `Skizze`, put one frame per sketched page showing the Figma screenshot: download it, `upload_asset` (local file), then a frame with just `<img src="…" style="width:100%">`, named `Skizze – <Seite>`. Reviewers compare sketch and result side by side. |

If the user names a canvas, use it.

**Re-runs.** If `Prototyp` already has frames named `<Seite> – Mobil` / `<Seite> – Desktop`, update those frames (`set_frame_html`, or stream with `start=true`) instead of adding new ones. Doop keeps version history. Check `updatedBy` first: if a human edited a frame after the last `Wien Revamp` build, ask before overwriting it.

## Steps

1. `get_guide` (`doop-instructions`) once. Where this file and the Doop guide disagree, follow this file: no inventing layouts, no stock imagery, no `search_icons`/`search_logos`/`generate_image`/`list_backgrounds`, no design brief or moodboard. The handbook is the design system.
2. `set_status`: "Skizze lesen → Wiener Melange Prototyp".
3. `set_guidelines`, named `Stadt Wien`: handbook markup only, theme bundle loaded, German copy taken from the sketch only, no invented contacts, prices, or dates, placeholders in `[Text fehlt]` form.
4. **Create every frame first, empty**, so you know all the frame ids before wiring links: for each page, `create_frame` `<Seite> – Mobil` (width 375) and `<Seite> – Desktop` (width 1440), height 3200, on `Prototyp`. Place Mobil frames in one row and Desktop frames in a row below (omit x/y if auto-placement does that).
5. Fetch the patterns you need with `scripts/fetch_pattern.py` (see [handbuch-fetch.md](handbuch-fetch.md)). Run `--version` first and use that version in [page-shell.md](page-shell.md).
6. **Stream each frame** with `append_frame_html`:
   - `start=true`: the head from page-shell.md, through `<body>`.
   - Header (whole, logo included), then `<main id="content">`, then the stage, then one chunk per region in sketch order, then `</main>`, then the footer with `done=true`, closing `body` and `html`.
   - Above each region, a comment linking it back to the sketch: `<!-- Skizze 12:14 [Karten x3 Bild] → card · Teaser Card (Standard) · Source: <pattern url> -->`.
   - Mobil and Desktop get the same markup. Only the `navigate:` frame ids differ (Mobil links to Mobil, Desktop to Desktop). Stream the first frame so viewers can watch it build. Send the other frames in one `set_frame_html` each, with the finished document and the ids swapped.
   - Fetch the header with `--compact`: the handbook header carries a ~12 KB demo mega-menu. Compact keeps the logo, search, menu button, and first-level menu and drops the nested demo submenus. Say so in the header's source comment.
7. **Review the stage first.** After the header and stage chunks of the first Mobil frame, call `get_frame_screenshot`. If the `wm-*` tags look unstyled, the module has not loaded yet: screenshot again before you change anything. If the font falls back to Lucida, say so. Do not swap fonts.
8. Finish all frames, then `get_frame_screenshot` every frame. Check, and fix with `edit_frame_html`:
   - every sketched box is present, in order, and nothing from the handbook demo leaked in (titles, "Lorem", demo photos, `#` links that should have had a sketch target);
   - grids have the sketched column count on Desktop and stack on Mobil;
   - no empty bands, clipped text, or unupgraded components;
   - frame height: the theme pins the footer to the bottom of the viewport, so a frame that is too tall shows a big white gap above the footer. Read where the last section ends on the screenshot, add about 200 px (Mobil) or 150 px (Desktop) for the footer, and `update_frame` to that height.
9. Wire click-through (below), then `set_prototype_start` on the first page's Mobil frame and `get_prototype`. Fix every target it flags.
10. Update the `Skizzen-Mapping` guideline with the final report plus frame ids. `set_status` to an empty string.

## Markup rules (from the handbook workflow)

- Every visible region comes from a fetched handbook sample. Keep the tags, slots, and attributes. Change only the text, `href`s, `src`s, and alt text.
- Replace the logo link `href` (the fetched header points at the handbook) with `https://www.wien.gv.at/`.
- Images: the handbook demo photos must not ship. An image slot without a sketch-supplied URL gets a Nebelgrau placeholder that keeps the slot:
  `<img slot="media" src="https://placehold.co/1200x450/F3F1EF/D6D1CA?text=Bild" alt="[Bild: <Beschriftung aus der Skizze>]">` (stage 1200x450, cards 800x450, list thumbnails 320x180; the light Nebelgrau label keeps it quiet)
  If placehold.co is blocked in the frame, use an inline `<div slot="media" style="aspect-ratio:16/9;background:#F3F1EF"></div>` and note it.
- Maps: a labelled placeholder (`[Stadtplan]`), never a drawn map.
- No CSS that restyles a component. The only allowed inline CSS is for a placeholder or a v1 gap, and it must be labelled in a comment.
- Heading order: one H1 (the stage), then H2 per section. Cards that are not under a section H2 use `h2` (the card page has h2 samples). Under a section H2 they use `h3`.
- Wrap each region that is not stage, tag list, or footer in `<wm-section>` (the theme's spacing). A highlighted section uses `highlight="nebelgrau"` (or the sketched color). The contact sample's `highlight="true"` stays as fetched.
- Missing text stays visible: `[Text fehlt]`, `[Überschrift fehlt]`, `[Link-Ziel fehlt]`.

## Click-through

Wire with Doop attributes on the element that triggers the step. The player does not follow `href`.

```html
<a href="#" data-doop-on="click" data-doop-action="navigate:<FRAME_ID>" data-doop-transition="push-left">Hallenbäder</a>
```

- For a clickable card (`wm-card clickable`), put the attributes on the heading link inside it, which is the element the card makes clickable.
- Links back to a parent page (`← Freizeit` tag, "zurück") use `data-doop-transition="push-right"`.
- External `→ https://…` links: keep the real `href` and add `data-doop-action="url:https://…"`.
- Header menu and footer links stay inert unless the sketch links them.
- Accordion, tabs, carousel, and menu behaviour come from the component JS. Do not wire them.

## Handoff

Return:

- the canvas link and the prototype player link `/c/<canvasId>/proto`;
- the pages built, with their Mobil and Desktop frame names;
- the theme version and the pattern URLs used;
- what the screenshots confirmed, and what still needs a human (open `[Text fehlt]` placeholders, missing link targets, keyboard and screen-reader checks, which a Doop frame cannot prove).

Claim only what you actually checked.
