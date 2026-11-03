# WorkflowMaster

Claude marketplace `stadt-wien-workflows`. The first plugin, `wien-sketch-to-prototype`, turns a rough tagged sketch from Figma or Doop into a clickable Doop prototype built from the official Wiener Melange web components on [handbuch.wien.gv.at](https://handbuch.wien.gv.at/pattern-library/patterns/).

People draw grey boxes, tag them (`[Bühne]`, `[Kacheln x3]`, German or English), and run `/wien-revamp <link>`. The skill maps each box, shows a mapping report, and builds mobile (375) and desktop (1440) frames from the handbook's `<wm-*>` markup and theme. Output goes to Doop only. Copy comes only from the sketch; missing text stays `[Text fehlt]`. Version 1 is content pages.

The decisions, live links, frame ids and open TODOs are in [HANDOFF.md](HANDOFF.md).

## Install

In Claude:

```
/plugin marketplace add https://github.com/dariob13/wien-sketch-to-prototype
/plugin install wien-sketch-to-prototype@stadt-wien-workflows
```

Figma and Doop are separate connectors. The steps are in [wien-sketch-to-prototype/docs/onboarding.md](wien-sketch-to-prototype/docs/onboarding.md).

From a checkout, check the marketplace before you commit:

```bash
claude plugin validate .
```

## Layout

```
.claude-plugin/marketplace.json          marketplace stadt-wien-workflows
HANDOFF.md                               project state for the next session
wien-sketch-to-prototype/
  .claude-plugin/plugin.json             plugin wien-sketch-to-prototype
  skills/wien-revamp/                    /wien-revamp
    SKILL.md                             workflow
    references/tag-vocabulary.md         source of truth: tag → pattern → variant
    references/                          sketch reading, fetch, Doop build, page shell
    scripts/fetch_pattern.py             handbook samples (python3 -I)
    scripts/selfcheck.py                 vocabulary vs. the live handbook
    scripts/figma-read-sketch.js         read-only Figma sketch reader
  docs/cheat-sheet.md                    German Spickzettel (keep in sync with the vocabulary)
  docs/cheat-sheet.html                  generated
  docs/onboarding.md                     German onboarding
  templates/                             Doop starter sketch; Figma file is linked from templates/README.md
```

## Changing a tag

`skills/wien-revamp/references/tag-vocabulary.md` is the source of truth. `docs/cheat-sheet.md` is the short German version of the same tags. Change both in the same commit. Then regenerate the HTML page:

```bash
python3 -I wien-sketch-to-prototype/docs/build_cheatsheet.py
```

Run Python with `-I` so a user site-packages install cannot change the result. The scripts use the standard library only.

After every Wiener Melange theme release, and after any vocabulary edit, run:

```bash
python3 -I wien-sketch-to-prototype/skills/wien-revamp/scripts/selfcheck.py
```

Exit 0 means the pinned theme version, every pattern slug, and every quoted variant name still match the live handbook, and every cheat-sheet tag is in the vocabulary. A quoted string is treated as a variant name only when it starts with an uppercase letter and is not a section title of the vocabulary (attribute values such as `"full"` and `"nebelgrau"`, and the cross-reference `"Text with no slot"`, are ignored).

`import_webpage` and `view_website` do not run the component JavaScript. Cards look flat and `wm-table` is invisible there. Judge styling from a Doop frame, which loads the theme script.
