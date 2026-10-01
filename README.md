# verny-tran.github.io

Personal site of Trần Trung Dũng (Verny), served by GitHub Pages from the `main` branch at [verny-tran.github.io](https://verny-tran.github.io).

Plain HTML and CSS with no build step, drawn in the visual language of the Pages résumé (`assets/resume.pdf`): the layout, spacing, colours and emphasis are measured from the PDF, at 1.6 CSS px per point.

- `index.html` opens with the résumé's two columns (portrait, contact, masthead, introduction), then shows the projects and the background as a bento grid of the résumé's cards: four columns, two below 900 px, one below 600 px.
- `projects/<name>/index.html` is one page per project: role, period, platform, links, an overview and the stack. Their icons are in `assets/icons/`, 256 px.
- Fonts are the résumé's own: SF Pro, SF Mono and New York on Apple devices, with Inter, JetBrains Mono and Source Serif 4 as fallbacks elsewhere.
- `assets/masthead.svg` holds the name and "iOS DEVELOPER" as outlines taken from the PDF, and the contact icons in `index.html` are the PDF's glyph outlines too.
- `corners.js` draws the résumé's continuous corners on every card and panel; without it the CSS border-radius is the fallback.
- On screens narrower than 900 px the two columns become one, with the smallest text sizes raised.

To add a project, copy one of the `projects/` pages, add its tile to the Projects grid in `index.html`, and list its URL in `sitemap.xml`.

## Custom domain

To move to a custom domain later (for example `verny.com`), add a `CNAME` file containing the domain, point its DNS at GitHub Pages, set the domain under Settings → Pages, and replace `https://verny-tran.github.io` in `index.html`, the `projects/` pages, `sitemap.xml` and `robots.txt`.
