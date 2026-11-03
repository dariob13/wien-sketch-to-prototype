# Page shell

Every prototype frame is one HTML document. Recheck the version string on [Erste Schritte](https://handbuch.wien.gv.at/development/erste-schritte/) (`Die aktuelle Version ist`) or the handbook footer before writing the URLs. The lines below are v2.10.0, confirmed on 2026-11-03.

```html
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Seitentitel | Stadt Wien</title>
  <link rel="stylesheet" href="https://assets.wien.gv.at/theme/v2.10.0/css/wiener-melange.bundle.min.css">
  <link rel="preload" href="https://assets.wien.gv.at/theme/v2.10.0/fonts/WienerMelangeVF.woff2" as="font" type="font/woff2" crossorigin>
  <script src="https://assets.wien.gv.at/theme/v2.10.0/js/bundle.min.js" type="module"></script>
</head>
<body>
  <!-- header pattern: the wien.gv.at variant, including its logo SVG -->
  <!-- main#content: stage, then the page's sections -->
  <!-- footer pattern -->
</body>
</html>
```

`bundle.min.js` registers the components. Prefer it to a hand-picked list of component files. Add single component modules only if a screenshot shows one tag still undefined after a second screenshot, using the URL pattern the handbook prints:

`https://assets.wien.gv.at/theme/v2.10.0/js/components/<Name>/<Name>.js`

The Erste Schritte page also shows a microsite header (`wm-nav-main microsite`, a site title, a short link list). That sample is for a special site, not for wien.gv.at. For a wien.gv.at page, fetch `/pattern-library/patterns/header/` and copy the variant whose heading matches the live header: logo, search, menu button.

Do not set a page background, a max-width wrapper, or a font on `body`. The theme does that. `lang="de"` stays even when a quoted English phrase appears in the content.

Relative handbook paths such as `/images/pattern/...` do not resolve inside a Doop frame. Prefix them with `https://handbuch.wien.gv.at` or replace them with the live page's absolute image URL.
