# Handoff: WorkflowMaster – Skizze → Wiener Melange Prototyp

Hand this whole file to the next agent. It is the full state of the project as of **2026-11-03**.

## 1. Goal (agreed with the user)

A workflow for a large mixed team (UX/UI designers, editors/Redaktion, developers, external agencies):

1. Someone draws a **rough sketch** (grey boxes) in **Figma or Doop**.
2. They write **tags** in the boxes, like `[Bühne]` or `[Kacheln x3]` (German or English, forgiving).
3. They run **`/wien-revamp <Figma- or Doop-Link>`** in Claude Code.
4. Claude maps every box to a **Wiener Melange** pattern from <https://handbuch.wien.gv.at/pattern-library/patterns/>, shows a mapping report, and builds a **clickable prototype in Doop** (375 Mobil + 1440 Desktop) from the official `<wm-*>` web-component markup and theme (`assets.wien.gv.at`, theme **v2.10.0**).

### Fixed decisions (do not re-ask)

| Topic | Decision |
|---|---|
| Input | Figma **or** Doop sketches |
| Output | **Doop only**. Never write to Figma, and never change the sketch. |
| Library | Website component library (handbuch.wien.gv.at HTML). **Not** the Wiener Melange Figma kit. |
| Users | Designers, Redaktion, devs/agencies. Everyone has Claude. Triggered by a skill command. |
| Tags | Forgiving: `[Tag]` in the box or the layer name, DE/EN, typos OK. Untagged boxes are guessed and marked as guesses. |
| Copy | **Only the sketch's text.** Never invent text. Missing text shows as `[Text fehlt]`. Never ship handbook demo text or photos. |
| Interaction | Click-through between pages plus built-in component behaviour |
| Breakpoints | Mobil 375 + Desktop 1440 from one sketch |
| Scope v1 | Content/topic pages. Forms and app screens become labelled gaps. |
| Deliverables | Revamp skill, tag cheat sheet, starter templates (Figma + Doop), onboarding guide |
| Distribution | Claude plugin in a git repo (marketplace) |
| Pilots | (1) sample sketch, (2) rough sketch of a live wien.gv.at page, compared with the original |
| Docs language | German for user docs (cheat sheet, onboarding). Skill internals in English. |

## 2. Repo layout (`/Users/dario/Documents/Projects/WorkflowMaster`, git initialised, first commit made)

```
.claude-plugin/marketplace.json          marketplace "stadt-wien-workflows" (validated with `claude plugin validate .`)
HANDOFF.md                               this file
wien-sketch-to-prototype/
  .claude-plugin/plugin.json             plugin v0.1.0
  skills/wien-revamp/
    SKILL.md                             main workflow (read sketch → map → report → fetch → build in Doop → hand off)
    references/
      tag-vocabulary.md                  SOURCE OF TRUTH: tags → pattern slug → variant, modifiers, slot rules
      sketch-reading.md                  reading Figma/Doop sketches, untagged-box heuristics, links/arrows
      mapping-report.md                  report format, when to ask, where the report goes
      build-in-doop.md                   Doop build steps, markup rules, click-through, frame heights
      handbuch-fetch.md, page-shell.md, pattern-index.md, foundations.md   (adapted from the user's stadt-wien-doop-prototyper skill)
    scripts/
      fetch_pattern.py                   python3 -I fetch_pattern.py <slug> [--list|--index n|--variant "…"|--compact|--version]
      figma-read-sketch.js               read-only use_figma script (replace __NODE_ID__); outputs a geometry-nested box tree, texts, links, arrows
  docs/
    cheat-sheet.md                       German "Spickzettel" (keep in sync with tag-vocabulary.md)
    cheat-sheet.html                     generated: python3 -I docs/build_cheatsheet.py
    build_cheatsheet.py
    onboarding.md                        German onboarding (setup, workflow, per-role tips, troubleshooting). Has placeholders <REPO-URL>, <KANAL/ISSUE-TRACKER>
  templates/
    doop/_style.css, startseite.html, hallenbaeder.html, vorlage-leer.html   Doop starter sketch source
    README.md                            where the Doop/Figma templates live
```

## 3. Live artifacts

| What | Where |
|---|---|
| Doop starter canvas + pilot 1 | https://doop.design/c/B-iDTpuPIM (pages "Skizze": sample sketch "Bäder in Wien" + "Hallenbäder" + "Vorlage - leer" + "Spickzettel"; "Prototyp": 4 finished frames, player https://doop.design/c/B-iDTpuPIM/proto; guidelines "Stadt Wien" + "Skizzen-Mapping") |
| Figma sketch file (starter template + pilot 2 sketch) | https://www.figma.com/design/BpjyDcUpLZ1Mtg0ScmcbSc (Personal plan, page "Skizzen": frames "Baden" 1:2, "Schwimmkurse" 1:76, "Vorlage – leer" 1:92, prototype link 1:48→1:76, arrow vector 1:106) |
| Doop pilot 2 | https://doop.design/c/vUy47I8paK (pages "Referenz" = import of https://www.wien.gv.at/freizeit/baden, "Skizze" = Figma screenshot, "Prototyp" = Baden/Schwimmkurse × Mobil/Desktop) |

Pilot 2 frame ids: Baden – Mobil `4BMM5fq-xc`, Schwimmkurse – Mobil `XdWAp7QdFi`, Baden – Desktop `QRPKTqvfi5`, Schwimmkurse – Desktop `g6JfjdL5cU`. All four have their HTML. Desktop heights are fitted (2560 / 640).

## 4. What the pilots proved

- Theme, Wiener Melange font, and `<wm-*>` components render in Doop frames. Header, stage, tags, cards, quicklinks, accordion, highlight, list, button, contact, and footer all look right on both widths.
- The Figma reader works: geometric nesting of text drawn over rectangles, X placeholders detected as images, prototype links resolved, canvas arrows resolved (arrow direction is guessed for LINE nodes).
- Tag inheritance (`[cards]` on the first of two boxes), group tags (`[Kachel x2]` around boxes), English tags, a typo (`[Stadtplann]`), and untagged header/pills/footer/4 boxes were all handled.
- Pilot 2 vs the live page: same section structure and order. Differences: live cards render without a shadow; live photos and the price table are absent (correct, because the sketch did not include them).

Lessons already written into the skill: the header Vorschau panel is only a template link (script resolves it), `--compact` header (the demo mega-menu is ~12 KB), the stage has no subtitle slot (move it to the Vorspann), optional sample parts get dropped, the `wm-grid size` → columns mapping, section `highlight="nebelgrau"`, frame height fitting (the footer sticks to the bottom), the placeholder image URL, and the handbook typo `scrollable"`.

## 5. Remaining TODO (in priority order)

1. ~~Finish pilot 2~~ **Done**: all 4 frames built and fitted, start frame set, `get_prototype` shows 6 interactions and 0 problems, "skizzen-mapping" guideline saved.
2. ~~templates/README.md~~ **Done**. Optional: save the Figma template drawing code as `templates/figma-starter.js`.
3. **Reduce output cost per run** (the biggest weakness): every frame repeats ~6 KB of header plus the footer. Idea: a local `scripts/build_page.py` that assembles the full HTML from a page spec (JSON) plus fetched samples, so the agent only writes the spec and pastes the generated file. Doop has no copy-frame tool and assets are images only, so the HTML still has to pass through a tool call. At least this removes hand-copy errors.
4. **Card shadow vs live**: check whether live wien.gv.at cards in plain sections use an attribute or class that removes the shadow (inspect `https://www.wien.gv.at/freizeit/baden` card markup and its CSS). If so, add it to the vocabulary.
5. Fill the placeholders in `docs/onboarding.md` (`<REPO-URL>`, `<KANAL/ISSUE-TRACKER>`) once the user has a remote repo. Ask the user for the git host and push only when asked.
6. Re-validate (`claude plugin validate .`), regenerate `docs/cheat-sheet.html`, and commit (end the commit message with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`).
7. Later (v2): forms (`formular-*` patterns), Sidebar, Sonderauftritte. Possibly a Figma plugin trigger for people without Claude.

## 6. Pilot 2 mapping report (for the "skizzen-mapping" guideline)

Baden: Header (Leiste, ohne Tag → Erkannt ~) · `[Stage mit Bild]` → stage Headerbild (ohne CTA), Bild Platzhalter · 6 Pills ohne Tag → Tags unter der Stage (Erkannt ~; „Alle Bäder ▾“ Dropdown ohne Optionen → normaler Tag) · `[cards]` + geerbt → 2 Cards in Grid l mit H3 + Quicklinks · `[Kachel x2]` → Saunabäder (Überschrift+Text), Schwimmkurse (Quicklinks; Überschrift → Seite Schwimmkurse via Figma-Prototyp-Link; „Alle Kurse und Angebote“ → Schwimmkurse via Pfeil, Richtung geschätzt) · `[Abschnitt grau]` → section nebelgrau mit 4 Cards (ohne Tag → Erkannt ~) · `[Stadtplann]` (Tippfehler → Stadtplan) → beschrifteter Kartenplatzhalter · `[Kontakt]` → kontakt ohne Newsletter/Social · Footer-Leiste → offizieller Footer (Skizze zeigt 3 Links). Offen: alle Link-Ziele `#` außer den Schwimmkurse-Links.
Schwimmkurse: Header (Leiste) · `[Bühne nur Titel]` · Pill „← Baden“ (Seitenname) → Zurück-Tag → Baden · `[Liste mit Links]` → Liste mit Links (Ziele fehlen) · Footer ergänzt.

## 7. Practical notes for the next agent

- Load the `figma-use` skill before any `use_figma` call. Doop needs `get_guide("doop-instructions")` once per session. Use `agent_name: "Wien Revamp"`.
- Figma: the user's only editable plan is **Personal** (`team::1687037167012492792`). The others are view seats.
- Doop page ids on the pilot canvases: `prototyp`, `skizze`, `<canvasId>:page1`.
- The shell can reach handbuch.wien.gv.at and www.wien.gv.at (curl works). Run Python with `-I`.
- The user's personal skills `stadt-wien-doop-prototyper` / `stadt-wien-figma-prototyper` live in `~/.claude/skills/`. Their `handbuch-fetch.md` still has the header bug (it copies the Vorschau link instead of the header). Tell the user; don't edit it without asking.
- Memory file: `~/.claude/projects/-Users-dario-Documents-Projects-WorkflowMaster/memory/wien-sketch-to-prototype-brief.md`.
