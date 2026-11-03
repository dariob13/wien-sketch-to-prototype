# Foundations

These notes are for checking a screenshot and for the rare gap that has no pattern. They are not styles to paste over a component. The theme CSS applies the real values. Recheck [colors](https://handbuch.wien.gv.at/look-and-feel/farben/), [typography](https://handbuch.wien.gv.at/look-and-feel/typography/), and the theme file when a number matters.

Measured against theme **v2.10.0** on 2026-10-16. A newer theme wins.

## Color

| Role | Token | Value |
| --- | --- | --- |
| Text, icons, table and quicklink borders | `--wm-color-fastschwarz` | `#292929` |
| Page, cards | `--wm-color-weiss` | `#FFFFFF` |
| Section highlight, stage placeholder, search field, table header | `--wm-color-nebelgrau-light` | `#F3F1EF` |
| Carousel-dot border, footer pipe | `--wm-color-nebelgrau` | `#D6D1CA` (paints near `#D5D0CA`) |
| Buttons, active dot, focus | `--wm-color-ui-interactive` | `#4B4B82` |
| Links | `--wm-color-ui-link` | `#1F4BAF` (paints near `#1F4CB2`) |
| Visited links | `--wm-color-ui-link-visited` | about `#AA1BB0` |
| Error / success | `--wm-color-ui-error` / `--wm-color-ui-success` | `#910000` / `#005738` |
| Logo only | `--wm-color-wien` | `#FF0000` |
| Notice | `--wm-color-wasserblau-light` / `--wm-color-wasserblau` | `#D2F0FF` / `#73CEE5` |
| Newsletter button | `--wm-color-frischgruen` | `#82D282` |

Text on white and on the light brand surfaces is `#292929`. White text is for Abendstimmung. Brand red is the logo. Do not assign a topic its own color.

## Space and type

Spacing tokens, in px at a 16 px root: `xxs 5`, `xs 10`, `s 15`, `m 20`, `l 30`, `xl 50`, `xxl 80`. Components take these as attributes such as `gap="m"`, when the fetched example does.

Desktop wrapper 1200 with 50 px padding, so the column is 1100 from 1024 px up. At 375 the padding is 15 and the column is 345. Breakpoints: 48em (768) and 64em (1024).

Corners are square, except tags (pill, 20) and carousel controls (circles). One shadow, from the theme, on the header and on cards. Cards inside a highlighted section have no shadow.

The type ramp below is what the live theme computed, so you can see a wrong heading. Do not restate it as inline font styles.

| Role | Desktop | Mobile | Weight |
| --- | --- | --- | --- |
| H1 in the stage | 32 / 41.6 | 28 / 36.4 | 700, tracking −1% |
| H2 of a section | 26 / 33.8 | 24 / 31.2 | 400 |
| H2 inside a card | 22.1 / 28.7 | same | 400 |
| Body in cards and lists | 17 / 25.5 | same | 400 |
| Standalone body | 17 / 28.9 | same | 400 |
| CTA and quicklink | 17 / 23 | same | 600 |
| Tag, table | 16 / 21.6 | same | 400, table tracking +2% |
| Footer copyright | 14 / 23.8 | same | 400 |

Font stack, already in the theme: Wiener Melange, then Lucida Sans Unicode, Lucida Grande, sans-serif. If the screenshot falls back to Lucida, the font request failed. Say so. Do not swap in another family to hide it.

## Icons

`<wm-icon iconid="...">` from the [icon pattern](https://handbuch.wien.gv.at/pattern-library/patterns/icon/). Typical ids on wien.gv.at: `burger`, `search`, `chevron-left`, `chevron-right`, `chevron-down`, `external`, `download`, `pin`, `clock`, `close`, `info`, `email`, `telefon`. Read the id off the example or the icon page. Sizes follow the component. Do not drop in a different icon set.
