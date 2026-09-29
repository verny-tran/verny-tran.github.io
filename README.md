# verny-tran.github.io

Personal site of Trần Trung Dũng (Verny), served by GitHub Pages from the `main` branch at [verny-tran.github.io](https://verny-tran.github.io).

The home page shows the résumé exactly as the PDF looks. Each page is an SVG drawing of `assets/resume.pdf`, with an invisible text layer on top, so the text can still be selected, searched and read by screen readers and search engines, and the links work.

## Updating the résumé

1. Export the résumé from Pages as PDF and save it over `assets/resume.pdf`.
2. Regenerate the pages:

   ```sh
   pip install pymupdf pillow
   python3 tools/pdf_to_site.py
   ```

   This rewrites `assets/resume/page-*.svg` and the pages section of `index.html`.
3. Commit and push to `main`.

## Custom domain

To move to a custom domain later (for example `verny.com`), add a `CNAME` file containing the domain, point its DNS at GitHub Pages, set the domain under Settings → Pages, and replace `https://verny-tran.github.io` in `index.html`, `sitemap.xml` and `robots.txt`.
