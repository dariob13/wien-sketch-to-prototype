# Onboarding: Von der Skizze zum Wiener-Melange-Prototyp

Du zeichnest graue Kästen, schreibst hinein, was sie sein sollen, und Claude baut daraus einen klickbaren Prototyp im echten wien.gv.at-Look, mobil und Desktop. Gebaut wird ausschließlich aus den offiziellen Wiener-Melange-Komponenten von [handbuch.wien.gv.at](https://handbuch.wien.gv.at/pattern-library/patterns/).

```
Skizze (Figma oder Doop)  →  /wien-revamp <Link>  →  Mapping-Tabelle  →  Prototyp in Doop
      du                         Claude               du prüfst          alle klicken durch
```

## 1. Einrichtung (einmalig, ca. 10 Minuten, ohne Terminal)

Du brauchst die Claude-Desktop-App oder claude.ai (Pro, Max, Team oder Enterprise), einen Doop-Account und, wenn du in Figma skizzierst, einen Figma-Account. Bei Team und Enterprise kann der Owner die Schritte für alle erledigen.

1. **Code-Ausführung einschalten:** Einstellungen, Capabilities, „Create and edit files“. Bei Team und Enterprise macht das der Owner unter Organization settings, Plugins & skills, Policy.
2. **Skill hochladen:** [`wien-revamp.zip`](https://github.com/dariob13/wien-sketch-to-prototype/raw/main/dist/wien-revamp.zip) herunterladen (nicht entpacken). Dann in Claude: Customize, Skills, „+“, „Create skill“, „Upload a skill“. Bei Team und Enterprise kann der Owner den Skill für alle bereitstellen.
3. **Doop verbinden:** Customize, Connectors, „+ Add“, „Add custom connector“, Name `Doop`, URL `https://doop.design/mcp`, dann im Browser anmelden.
4. **Figma verbinden:** Figma im Connector-Verzeichnis suchen und verbinden. Alternativ als eigener Connector mit `https://mcp.figma.com/mcp`.
5. **Im Chat:** unten links „+“, Connectors, Doop und Figma einschalten.

**Test:** `Nutze wien-revamp: <Link zur Beispielskizze>` schreiben (siehe [Vorlagen](../templates/README.md)). Nach ein paar Minuten kommt ein Doop-Link.

In Claude Code heißt der Befehl `/wien-revamp <Link>`. Das Plugin installiert man dort mit `/plugin marketplace add https://github.com/dariob13/wien-sketch-to-prototype` und `/plugin install wien-sketch-to-prototype@stadt-wien-workflows`.

Die ausführliche Anleitung als PDF: [guides/anleitung-sketch-skill.pdf](../../guides/anleitung-sketch-skill.pdf).

## 2. Der Ablauf für alle

1. **Vorlage kopieren** (Figma-Datei oder Doop-Canvas aus [templates](../templates/README.md)). Neben der Vorlage liegt der Spickzettel.
2. **Pro Seite ein Frame.** Den Frame so benennen, wie die Seite heißt, zum Beispiel `Startseite` oder `Hallenbad-Detail`.
3. **Kästen zeichnen**, von oben nach unten in der Reihenfolge der Seite. Grau, schwarz-weiß, schief: alles egal.
4. **Tags hineinschreiben**: `[Bühne]`, `[Kacheln x3]`, `[Quicklinks]`, siehe [Spickzettel](cheat-sheet.md).
5. **Echten Text dazuschreiben.** Erste Zeile = Überschrift. Was du nicht schreibst, steht später als `[Text fehlt]` da. Die KI erfindet keine Texte.
6. **Verlinken:** `→ Hallenbad-Detail` in den Kasten schreiben oder eine Figma-Prototyp-Verbindung ziehen.
7. **In Claude:** `/wien-revamp <Link zur Figma-Seite oder zum Doop-Canvas>`.
8. **Tabelle prüfen.** Claude zeigt für jeden Kasten, was daraus wird, und markiert, was nur geraten ist (`Erkannt ~`, `Unsicher ?`). Bei echten Unklarheiten fragt Claude kurz nach.
9. **Prototyp ansehen.** Claude liefert zwei Links: den Doop-Canvas (zum Kommentieren) und den Player (zum Durchklicken).
10. **Ändern:** Skizze anpassen und denselben Befehl noch einmal ausführen. Die Prototyp-Frames werden aktualisiert, frühere Stände bleiben in Doops Versionsverlauf.

**Tipp:** Je mehr Tags, desto weniger Raten. Ein Tag pro Kasten ist die sicherste Variante.

## 3. Für Designer*innen

- Ihr könnt Figma-Prototyp-Verbindungen nutzen: Die werden zu Klickpfaden in Doop. Pfeile zwischen Frames funktionieren auch, sind aber weniger zuverlässig.
- Bestehende Wireframe-Kits funktionieren. Komponentennamen wie `Card` oder `Button` gelten als Hinweis, sind aber kein Muss.
- Wollt ihr eine bestimmte Variante, schreibt sie als Zusatz: `[Bühne farbig]`, `[Akkordeon eins offen]`, `[Hervorhebung Rahmen]`. Alle Zusätze stehen im Spickzettel.
- Der Prototyp verwendet keine eigenen Styles. Sieht etwas falsch aus, liegt es fast immer am gewählten Pattern. Ändert dann den Tag und lasst es neu laufen, statt im Doop-HTML zu stylen.

## 4. Für die Redaktion

- Ihr müsst nicht zeichnen können. Rechtecke untereinander reichen völlig.
- Schreibt den echten Text in die Kästen. Der landet 1:1 im Prototyp, auch mit Tippfehlern. Claude listet diese auf, korrigiert sie aber nicht.
- Kontaktdaten, Preise, Öffnungszeiten und Termine kommen **nur** aus eurer Skizze. Fehlen sie, steht da ein Platzhalter. So entsteht nie etwas Falsches, das echt aussieht.
- Unsicher, welcher Tag passt? Schreibt `[?]` und Claude macht einen Vorschlag.

## 5. Für Entwickler*innen und Agenturen

- Der Prototyp ist **kein Produktionscode**, aber das Markup stammt 1:1 aus dem Handbuch (`<wm-*>`-Komponenten, Theme-CSS und `bundle.min.js` von `assets.wien.gv.at`).
- Über jeder Region steht ein Kommentar: Skizzen-Element → Pattern → Variante → Quell-URL. Die vollständige Zuordnung liegt im Doop-Canvas als Guideline `Skizzen-Mapping`.
- Die Theme-Version steht im `<head>` jedes Frames. Prüft sie gegen die [aktuelle Version](https://handbuch.wien.gv.at/development/erste-schritte/).
- Freigaben laufen über den Doop-Status `ready_for_dev`. Jede Änderung am Frame hebt die Freigabe auf.
- Doop kann Tastatur- und Screenreader-Verhalten nicht nachweisen. Das bleibt eure Prüfung.

## 6. Wenn etwas nicht klappt

| Problem | Lösung |
| --- | --- |
| „Figma/Doop ist nicht verbunden“ | `/mcp` → Authenticate. In der Desktop-App: Connectors prüfen. |
| Claude findet die Seite nicht | Den Link mit `node-id=…` kopieren: in Figma Rechtsklick auf den Frame oder die Seite → *Copy link*. |
| Ein Kasten wurde falsch erkannt | Einen Tag hineinschreiben und neu ausführen. |
| Komponenten sehen ungestylt aus | Kurz warten und neu laden. Bleibt es so, Claude bitten, die Screenshots zu wiederholen. |
| Schrift sieht anders aus (Lucida) | Die Wiener-Melange-Schrift wurde nicht geladen. Das ist ein Ladeproblem, kein Designfehler. Claude meldet es. |
| Ich will nur eine Seite neu bauen | `/wien-revamp <Link> nur Startseite` |
| Mein Doop-Frame wurde überschrieben | In Doop: Versionsverlauf des Frames → alte Version wiederherstellen. |

## 7. Grenzen der Version 1

- Nur Inhalts- und Themenseiten. Formulare, Sidebar und Sonderauftritte werden als markierte Lücke gebaut.
- Bilder sind Platzhalter, außer du gibst eine Bild-URL an (`Bild: https://…`).
- Ausgabe nur nach Doop. Figma dient nur zum Skizzieren.

## 8. Feedback und Updates

Fehlerhafte Erkennungen bitte mit Link zur Skizze und zum Prototyp als Issue im Plugin-Repo melden: https://github.com/dariob13/wien-sketch-to-prototype/issues. Neue Tags oder Synonyme kommen in `skills/wien-revamp/references/tag-vocabulary.md` **und** in den Spickzettel. Updates holt ihr mit `/plugin marketplace update stadt-wien-workflows`.
