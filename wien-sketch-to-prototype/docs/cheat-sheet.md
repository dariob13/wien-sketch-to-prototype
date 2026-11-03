# Spickzettel: Skizze → Wiener Melange

**So geht's:** Kästen zeichnen → Tag in eckigen Klammern hineinschreiben → echten Text dazuschreiben → in Claude `/wien-revamp <Link>` eingeben.

```
Ein Kasten:
  [Bühne mit Bild]              <- Tag in eckigen Klammern
  Baden in Wien                 <- 1. Zeile = Überschrift
  Alle Bäder auf einen Blick    <- weitere Zeilen = Text
  → Hallenbäder                 <- Klick führt zur Seite "Hallenbäder"

Drei gleiche Kästen nebeneinander = 3 Spalten.
Tag nur im ersten Kasten reicht, oder [Kacheln x3] im Rahmen drumherum.
```

## Regeln

- **Tag** = `[Wort]` im Kasten oder im Ebenennamen. Deutsch oder Englisch, Groß-/Kleinschreibung egal, Umlaute egal, kleine Tippfehler auch.
- **Zusätze** in dieselbe Klammer: `[Kacheln x3 mit Bild]`, `[Abschnitt grau]`, `[Bühne nur Titel]`.
- **Ohne Tag** rät die KI anhand der Form und sagt dir, was sie geraten hat. Mit Tag ist es sicher.
- **Text:** Es wird nur dein Text verwendet. Fehlt Text, steht im Prototyp `[Text fehlt]`.
- **Header und Footer** kommen automatisch dazu. Du musst sie nicht zeichnen.
- **Bilder:** `(Bild)` oder einen Kasten mit X zeichnen. Daraus wird ein grauer Bildplatzhalter.
- **Links:** `→ Seitenname` in den Kasten schreiben. Oder in Figma eine Prototyp-Verbindung ziehen, oder einen Pfeil zum anderen Frame.
- **Jede Seite** ist ein eigener Frame. Der Frame-Name ist der Seitenname.

## Tags

| Schreib | Oder auch | Wird zu |
| --- | --- | --- |
| `[Bühne]` | Stage, Hero, Titelbild | Großer Seitenkopf mit H1 |
| `[Tags]` | Schlagworte, Themen | Tag-Leiste, `← Freizeit` = Zurück-Tag |
| `[Vorspann]` | Intro, Einleitung | Einleitungstext |
| `[Inhalt]` | Sprungnavigation, TOC | Inhaltsverzeichnis der Seite |
| `[Meldung]` | Hinweis, Warnung, Fehler, Erfolg | Meldungsbalken |
| `[Abschnitt]` | Section, Bereich | Abschnitt mit H2. `grau` = hinterlegt |
| `[Kachel]` | Card, Teaser, Box | Card. `x3` = 3 Stück, `mit Bild`, `farbig`, `nur Titel` |
| `[Karussell]` | Slider, Carousel | Blätterbare Cards |
| `[Infobox]` | Steckbrief, Fakten | Infobox mit `Label: Wert`-Zeilen |
| `[Hervorhebung]` | Kasten, Wichtig, Callout | Farbiger Kasten. `gelb`, `grün`, `blau`, `grau`, `Rahmen` |
| `[Zitat]` | Quote | Zitat. `— Name` = Autor*in |
| `[Kontakt]` | Ansprechperson | Kontaktblock (nur deine Daten!) |
| `[Newsletter]` | Abo | Newsletter-Anmeldung. Mit Kontakt: Kontaktblock inklusive Newsletter |
| `[Quicklinks]` | Wichtige Links | Linkliste mit Pfeilen. `3 Spalten` |
| `[Liste]` | Aufzählung, Bullets | Liste. `nummeriert` |
| `[Linkliste]` | Weiterführende Links | Liste mit Links |
| `[Termine]` | Veranstaltungen, Events | Event-Liste |
| `[Mehr-Link]` | CTA, Weiterlesen | Hervorgehobener Link mit Pfeil |
| `[Button]` | Knopf | Button. `sekundär`, `tertiär` |
| `[Download]` | PDF, Datei | Download-Link |
| `[Reiter]` | Tabs | Registerkarten |
| `[Akkordeon]` | FAQ, Aufklapper | Aufklappliste. `+ Frage` je Eintrag |
| `[Tabelle]` | Öffnungszeiten, Preise | Tabelle. In einer Card wird daraus „Tabelle in Card“. Spalten mit `\|` trennen |
| `[Bild]` | Foto, Image | Bild (Platzhalter) |
| `[Galerie]` | Bilder | Bildergalerie |
| `[Video]` | Film | Videoplayer |
| `[Audio]` | Podcast | Audioplayer |
| `[Stadtplan]` | Map, Lageplan | Kartenplatzhalter |
| `[Trenner]` | Linie, Divider | Trennlinie |
| `[Zeitstempel]` | Zuletzt geändert | „Zuletzt geändert“-Zeile |
| `[Seiten]` | Paginierung | Seitenzahlen |
| `[Suche]` | Suchfeld | Suchfeld im Header. `Filter` → Filter, `Vorschläge` → Combobox, `Ergebnisse` → Cards |

**Achtung „Karte“:** Das kann eine Card oder einen Stadtplan meinen. Schreib besser `[Kachel]`/`[Card]` oder `[Stadtplan]`/`[Map]`.

## Sonder-Tags

| Schreib | Bedeutung |
| --- | --- |
| `[Notiz] …` | Hinweis an die KI. Wird befolgt, aber nicht gebaut. |
| `[?]` | „Weiß nicht, schlag was vor.“ |
| `[aus]` | Diesen Kasten überspringen |
| `[ohne Header]` / `[ohne Footer]` | Header/Footer weglassen |

## Kommt später (Version 2)

Formulare (Eingabefelder, Checkboxen, Auswahl, Upload, Schritte), Sidebar, Sonderauftritte. Diese Tags werden erkannt und als markierte Lücke gebaut.

## Befehl

```
/wien-revamp https://www.figma.com/design/…?node-id=12-3
/wien-revamp https://doop.design/c/…
/wien-revamp <Link> nur Startseite
```

Danach siehst du eine Tabelle (Kasten → Pattern) und bekommst einen Link zum Doop-Prototyp, mobil und Desktop, klickbar.
