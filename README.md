# verny-tran.github.io

Personal site of Trần Trung Dũng (Verny), served by GitHub Pages from the `main` branch at [verny-tran.github.io](https://verny-tran.github.io).

Plain HTML and CSS with no build step, drawn in the visual language of the Pages résumé (`assets/resume.pdf`): the layout, spacing, colours and emphasis are measured from the PDF, at 1.6 CSS px per point.

- `index.html` is one bento grid of the résumé's cards that follows the window: six columns from 1500 px, four from 900 px, two from 600 px, one below, up to 1800 px wide. The opening (portrait in the top left corner, masthead, introduction, contact, links) is laid out with grid areas per width; the projects and background follow, with short cards stacked in a `.cell` so a row never stretches far past its content.
- `projects/<name>/index.html` is one page per project: role, period, platform, links, an overview and the stack. Their icons are in `assets/icons/`, 256 px.
- Fonts are the résumé's own: SF Pro, SF Mono and New York on Apple devices, with Inter, JetBrains Mono and Source Serif 4 as fallbacks elsewhere.
- `assets/masthead.svg` holds the name and "iOS DEVELOPER" as outlines taken from the PDF, and the contact icons in `index.html` are the PDF's glyph outlines too.
- `corners.js` draws the résumé's continuous corners on every card and panel; without it the CSS border-radius is the fallback.
- On screens narrower than 900 px the two columns become one, with the smallest text sizes raised.

To add a project, copy one of the `projects/` pages, add its tile to the Projects grid in `index.html`, and list its URL in `sitemap.xml`.

Every page links `styles.css` and `corners.js` with `?v=` and the first eight hex digits of the file's SHA-256 (`shasum -a 256 styles.css`). GitHub Pages lets browsers cache both for ten minutes, so after changing either file, put its new hash in every page and in `404.html`; otherwise new markup can meet the old stylesheet and the grid falls apart.

## Custom domain

To move to a custom domain later (for example `verny.com`), add a `CNAME` file containing the domain, point its DNS at GitHub Pages, set the domain under Settings → Pages, and replace `https://verny-tran.github.io` in `index.html`, the `projects/` pages, `sitemap.xml` and `robots.txt`.
