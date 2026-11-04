# Mapping report

The report is the contract between the sketcher and the build. Show it **before** building, in the user's language (German labels by default). Keep it short enough to read in a minute.

## Format

```markdown
## Skizze → Wiener Melange: Startseite

| # | Kasten (Skizze) | Gelesen als | Pattern · Variante | Basis | Hinweis |
|---|---|---|---|---|---|
| 1 | — | Header (ergänzt) | header · wien.gv.at | Standard | Nicht gezeichnet, automatisch ergänzt |
| 2 | „Baden in Wien“ | [Bühne] | stage · Stage mit Headerbild, Titel und hervorgehobenem Link | Tag ✓ | Bild: Platzhalter |
| 3 | 3 Pills | (ohne Tag) | tag · Tags unter der Stage | Erkannt ~ | |
| 4 | „Hallenbäder“, … | [Karten x3 Bild] | card · Teaser Card (Standard) ×3 | Tag ✓ | Karte 2: Text fehlt |
| 5 | Kasten unten links | (ohne Tag) | section · H2 + Text | Unsicher ? | Oder: Kontakt? |
| 6 | — | Footer (ergänzt) | footer | Standard | |

**Links:** Karte 1 → „Bad-Detail“ (Prototyp-Verbindung) · „Mehr →“ → [Link-Ziel fehlt: Alle Bäder]
**Text fehlt:** Karte 2 (Text), Bühne (Link-Beschriftung)
**Tippfehler (nicht korrigiert):** „Hallenbder“ in Karte 1
**Nicht in Version 1:** [Formular] in Kasten 7, als markierte Lücke gebaut
**Icons:** Karte 2 → Piktogramm „Telefon“ · `(Icon: Rakete)` → kein Treffer, weggelassen
**Illustrationen:** Bühne → „Schwimmbad“ (Freigabe Handbuch-Team nötig)
**Notizen der Skizze:** „Link-Ziele kommen noch“ (befolgt: Links bleiben leer)
```

Basis values:

- `Tag ✓`: the sketcher wrote the tag (also a layer name, or a bare pattern word, plus a note saying so).
- `Erkannt ~`: no tag, but a shape rule clearly fits.
- `Unsicher ?`: a guess. Give the alternative in Hinweis.
- `Standard`: added by the workflow (header, footer).

Number rows in page order. Nested items (cards inside a section) take `4.1`, `4.2`.

## When to stop and ask

Ask before building (one `AskUserQuestion` with concrete options, at most four questions) only when an answer changes the **structure**:

- a box marked `Unsicher ?` whose alternatives are different patterns,
- an unknown tag with no clear nearest entry,
- an ambiguous `[Karte]` that context does not settle,
- a link target that might be a page the user forgot to include.

Do **not** stop for missing text, typos, missing images, the added header and footer, or v1 gaps. Those are in the report and get built as visible placeholders.

With no blocking question, show the report and build straight away in the same turn.

## Where the report goes

1. In the chat, before the build.
2. On the Doop canvas, as a guideline named `Skizzen-Mapping`, updated after the build with the final pattern list and the Doop frame ids. Developers and agencies read the mapping there.
3. In the handoff at the end, shortened to what changed or stayed open.
