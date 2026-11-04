---
name: wien-revamp
description: Turn a rough, tagged sketch (a Figma or Doop link) into a clickable Stadt Wien prototype in Doop built from the official Wiener Melange web components on handbuch.wien.gv.at. Use when someone shares a Figma or Doop sketch, wireframe, or "Skizze" and wants it revamped, translated, cleaned up, or turned into a real wien.gv.at-style prototype, or types /wien-revamp. Not for briefs without a sketch, other websites, or production code.
argument-hint: <Figma- oder Doop-Link> [nur <Seitenname>]
---

# Wien Revamp: Skizze → Wiener Melange Prototyp

Someone drew grey boxes and wrote tags like `[Bühne]` or `[Karten x3]` in them. Read the sketch, map every box to a Wiener Melange pattern, show the mapping, then build the page in Doop from real handbook markup, for mobile (375) and desktop (1440), with click-through between pages.

The people using this include designers, editors (Redaktion), developers, and external agencies. Many of them are not designers. Be forgiving when you read the sketch, and strict when you build.

## Fixed decisions

- **Input:** a Figma link (`figma.com/design/…`) or a Doop link (`doop.design/c/…`). With no link, ask for one. With a brief and no sketch, say this skill needs a sketch (the `stadt-wien-doop-prototyper` skill, if installed, builds from briefs).
- **Output:** Doop only. Never write to Figma, and never change the sketch.
- **Library:** the Wiener Melange web components from handbuch.wien.gv.at, loaded from `assets.wien.gv.at`. Not the Figma kit, not your own CSS.
- **Copy:** the sketch's text only. Never write new copy. Never ship handbook demo text. Missing text stays a visible `[Text fehlt]`.
- **Scope v1:** content and topic pages. Forms and app screens become labelled gaps.

## Workflow

1. **Read the sketch.** Follow [references/sketch-reading.md](references/sketch-reading.md). Figma: `create_session`, load the `figma-use` skill if your client has it, run [scripts/figma-read-sketch.js](scripts/figma-read-sketch.js) through `use_figma`, and take a screenshot of every page frame. Doop: `get_canvas`, `get_frame`, `get_frame_screenshot`. If the user wrote `nur <Seite>`, read only that page plus what you need to resolve its links.
2. **Map every box.** Use [references/tag-vocabulary.md](references/tag-vocabulary.md): tag → pattern → variant, and box text → slots. Guess untagged boxes with the rules in sketch-reading.md, and label every guess as one.
3. **Show the mapping report** ([references/mapping-report.md](references/mapping-report.md)). Ask only questions that change the structure (unsure pattern, unknown tag, ambiguous `[Karte]`, a possibly forgotten page), in one short question (`AskUserQuestion` where the client has it). Otherwise go straight on.
4. **Pick icons and illustrations** only from the handbook catalogs: `python3 -I scripts/fetch_assets.py icons <Wort>` / `illustrationen <Wort>` ([references/icons-illustrations.md](references/icons-illustrations.md)).
5. **Fetch the patterns.** Run `python3 -I scripts/fetch_pattern.py --version`, then fetch each needed pattern and variant. With no network or no shell (the Claude app), read the bundled copies in `references/samples/<slug>.html` instead ([references/handbuch-fetch.md](references/handbuch-fetch.md), [references/pattern-index.md](references/pattern-index.md)). The handbook sample wins over anything remembered.
6. **Build in Doop.** Follow [references/build-in-doop.md](references/build-in-doop.md): create all frames first, stream the official markup with the page shell from [references/page-shell.md](references/page-shell.md), check the screenshots, fit the heights, wire click-through, and set the prototype start.
7. **Hand off.** Canvas link, player link, what was built, what is open, what a human still has to check. Save the final mapping as the `Skizzen-Mapping` guideline on the canvas.

No terminal is needed on the user's side. In the Claude app the scripts run in Claude's own code sandbox, if it is enabled. Without network there, use the bundled snapshot and catalogs. Run `fetch_pattern.py` with this skill's own directory (the folder this SKILL.md is in) as the script path.

## Rules that are easy to get wrong

- **Icons and illustrations:** only from <https://handbuch.wien.gv.at/look-and-feel/icons-und-illustrationen/icons/> and <https://handbuch.wien.gv.at/look-and-feel/icons-und-illustrationen/illustrationen/>. Never `search_icons`, other sets, emoji, or generated art. UI icons inside a fetched sample (chevrons, burger, search) stay as `wm-icon`. Every icon you *choose* is a pictogram `<img>`. Illustrations need Handbuch-team sign-off, so report them.

- **Header and footer** are added even when they are not sketched (official chrome). Their labels are official, not invented copy.
- **"Karte"** can mean a card or a map. Decide from context and say which reading you chose.
- **Counts:** `x3` sets the item count and the desktop columns. Three equal boxes side by side mean three columns even when no count is written.
- **Images:** a sketch image or X becomes a Nebelgrau placeholder. No stock, generated, or handbook demo photos.
- **Contacts, prices, opening hours, dates:** only from the sketch. Never fill them in from the web or from memory.
- **The header sample** comes from the template page. The pattern page's Vorschau panel is only a link (the script handles this).
- **Doop's generic design advice** (moodboards, briefs, stock imagery, logo search, "realistic placeholder copy") does not apply here. The handbook and the sketch are the brief.

## Foundations

[references/foundations.md](references/foundations.md) lists the theme colors, spacing, breakpoints, and the type ramp. Use it to judge screenshots and to style the rare labelled placeholder. Never paste it over a component.
