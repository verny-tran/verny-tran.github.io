#!/usr/bin/env python3
"""Build the site's résumé pages from assets/resume.pdf.

Each PDF page becomes two layers that line up exactly:

- assets/resume/page-N.svg: the page drawn as vectors, with text turned into
  glyph outlines, so it looks identical to the PDF on every device.
- An inline <svg> text layer in index.html: the same text, invisible, with
  every character at its PDF position, so it can be selected, copied,
  searched and read by screen readers and search engines. Links from the PDF
  and the contact lines sit on top of it.

Usage, after exporting a new PDF from Pages to assets/resume.pdf:

    pip install pymupdf pillow
    python3 tools/pdf_to_site.py

The script rewrites the SVG files and the part of index.html between the
"pages" markers.
"""

import base64
import html
import io
import re
from pathlib import Path

import pymupdf
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "assets" / "resume.pdf"
OUT = ROOT / "assets" / "resume"
INDEX = ROOT / "index.html"
START = "<!-- pages:start -->"
END = "<!-- pages:end -->"

# Contact lines in the PDF carry no links; match them by their text.
CONTACT_LINKS = [
    ("(+84) 86.887.3841", "tel:+84868873841"),
    ("vernytran@icloud.com", "mailto:vernytran@icloud.com"),
    ("linkedin.com/in/vernytran", "https://www.linkedin.com/in/vernytran"),
    ("github.com/verny-tran", "https://github.com/verny-tran"),
]


def fmt(value):
    text = f"{value:.2f}".rstrip("0").rstrip(".")
    return "0" if text == "-0" else text


def shrink_numbers(svg):
    """Round long decimals outside data URIs; 0.001 of a unit is invisible."""
    parts = re.split(r'(data:[^"]+)', svg)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r"(-?\d*\.\d{4,})", lambda m: f"{float(m.group(1)):.3f}".rstrip("0").rstrip("."), parts[i])
    return "".join(parts)


def recompress_photos(svg):
    """Store large opaque PNGs (the portrait) as JPEG; keep small ones as they are."""
    def replace(match):
        raw = base64.b64decode(match.group(1))
        if len(raw) < 100_000:
            return match.group(0)
        image = Image.open(io.BytesIO(raw))
        if image.mode not in ("RGB", "L"):
            return match.group(0)
        buffer = io.BytesIO()
        image.convert("RGB").save(buffer, "JPEG", quality=90, optimize=True, progressive=True)
        return 'xlink:href="data:image/jpeg;base64,' + base64.b64encode(buffer.getvalue()).decode() + '"'

    return re.sub(r'xlink:href="data:image/png;base64,([^"]+)"', replace, svg)


def page_svg(page):
    svg = page.get_svg_image(text_as_path=True)
    svg = re.sub(r' data-text="[^"]*"', "", svg)
    svg = recompress_photos(svg)
    svg = shrink_numbers(svg)
    width, height = fmt(page.rect.width), fmt(page.rect.height)
    svg = re.sub(r'<svg ([^>]*?)width="[^"]*" height="[^"]*"', rf'<svg \1width="{width}" height="{height}"', svg, count=1)
    return svg


def text_layer(page):
    """One <text> per span, with an x position for every character."""
    lines = []
    for block in page.get_text("rawdict")["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            if line["dir"] != (1.0, 0.0):
                continue
            for span in line["spans"]:
                chars = [c for c in span["chars"] if c["c"] not in "​"]
                if not "".join(c["c"] for c in chars).strip():
                    continue
                # SF Symbols icons live in the Private Use Area; skip them.
                chars = [c for c in chars if not 0xE000 <= ord(c["c"]) <= 0xF8FF and ord(c["c"]) < 0xF0000]
                if not chars:
                    continue
                xs = " ".join(fmt(c["origin"][0]) for c in chars)
                y = fmt(chars[0]["origin"][1])
                text = html.escape("".join(c["c"] for c in chars), quote=False)
                lines.append(f'<text x="{xs}" y="{y}" font-size="{fmt(span["size"])}">{text}</text>')
    return lines


def link_boxes(page):
    boxes = []
    for link in page.get_links():
        if link.get("uri"):
            boxes.append((link["uri"], link["from"]))
    for needle, uri in CONTACT_LINKS:
        for rect in page.search_for(needle):
            boxes.append((uri, rect))
    rects = []
    for uri, r in boxes:
        rects.append(
            f'<a href="{html.escape(uri)}"><rect x="{fmt(r.x0)}" y="{fmt(r.y0)}" '
            f'width="{fmt(r.width)}" height="{fmt(r.height)}"/></a>'
        )
    return rects


def main():
    doc = pymupdf.open(PDF)
    OUT.mkdir(parents=True, exist_ok=True)
    sheets = []
    for number, page in enumerate(doc, start=1):
        (OUT / f"page-{number}.svg").write_text(page_svg(page), encoding="utf-8")
        w, h = fmt(page.rect.width), fmt(page.rect.height)
        layer = "\n                ".join(text_layer(page) + link_boxes(page))
        sheets.append(
            f'''        <section class="sheet" aria-label="Résumé page {number}">
            <img src="/assets/resume/page-{number}.svg" width="{w}" height="{h}" alt="" {'fetchpriority="high"' if number == 1 else 'loading="lazy"'}>
            <svg class="text-layer" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
                {layer}
            </svg>
        </section>'''
        )

    index = INDEX.read_text(encoding="utf-8")
    block = START + "\n" + "\n".join(sheets) + "\n        " + END
    index = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, index, flags=re.S)
    INDEX.write_text(index, encoding="utf-8")
    print(f"Wrote {len(doc)} pages to {OUT.relative_to(ROOT)} and updated {INDEX.name}")


if __name__ == "__main__":
    main()
