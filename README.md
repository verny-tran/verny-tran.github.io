# verny-tran.github.io

Personal site of Trần Trung Dũng (Verny), served by GitHub Pages from the `main` branch at [verny-tran.github.io](https://verny-tran.github.io).

Plain HTML and CSS with no build step. The page is a web version of the Pages résumé (`assets/resume.pdf`): the layout, spacing, colours and emphasis are measured from the PDF, at 1.6 CSS px per point.

- Fonts are the résumé's own: SF Pro, SF Mono and New York on Apple devices, with Inter, JetBrains Mono and Source Serif 4 as fallbacks elsewhere.
- `assets/masthead.svg` holds the name and "iOS DEVELOPER" as outlines taken from the PDF, and the contact icons in `index.html` are the PDF's glyph outlines too.
- On screens narrower than 900 px the two columns become one, with the smallest text sizes raised.

## Custom domain

To move to a custom domain later (for example `verny.com`), add a `CNAME` file containing the domain, point its DNS at GitHub Pages, set the domain under Settings → Pages, and replace `https://verny-tran.github.io` in `index.html`, `sitemap.xml` and `robots.txt`.
