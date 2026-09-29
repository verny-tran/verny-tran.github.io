/* Continuous corners, as Pages draws them in the résumé PDF.
 *
 * CSS border-radius draws circular arcs, and corner-shape is not in Safari
 * or Firefox, so every card, panel and the portrait gets its outline here:
 * the element's ground is clipped to the continuous shape and its border is
 * stroked by an SVG laid over it. Without this script the CSS border-radius
 * corners stay as the fallback.
 *
 * The corner is the PDF's own: three cubic Béziers per corner, measured
 * from the résumé and scaled by the corner's extent, the distance from the
 * corner at which the straight edge starts to bend.
 */
(function () {
    // Points of one corner as (back along the incoming edge, along the
    // outgoing edge), in units of the extent: start, then 3 × (c1, c2, end).
    var CORNER = [
        [1, 0],
        [0.70652, 0], [0.53048, 0], [0.41309, 0.049],
        [0.24388, 0.11059], [0.11059, 0.24388], [0.049, 0.41309],
        [0, 0.53048], [0, 0.70652], [0, 1]
    ];

    // Extents in CSS px at 1.6 px per point: cards 23.8 pt, the portrait
    // 22.9 pt, panels 14.9 pt, all measured on the stroke's centre line.
    var SHAPES = [
        { selector: ".portrait", extent: 36.7 },
        { selector: ".inner", extent: 23.9 },
        { selector: ".card", extent: 38.1 }
    ];

    var SVG = "http://www.w3.org/2000/svg";

    function round(n) {
        return Math.round(n * 100) / 100;
    }

    // The outline of a w × h box inset by `inset`, clockwise from the top
    // edge, with continuous corners of the given extent.
    function outline(w, h, extent, inset) {
        var e = Math.max(0, Math.min(extent, (w - 2 * inset) / 2, (h - 2 * inset) / 2));
        var corners = [
            { x: w - inset, y: inset, d1: [1, 0], d2: [0, 1] },
            { x: w - inset, y: h - inset, d1: [0, 1], d2: [-1, 0] },
            { x: inset, y: h - inset, d1: [-1, 0], d2: [0, -1] },
            { x: inset, y: inset, d1: [0, -1], d2: [1, 0] }
        ];
        var d = "";
        corners.forEach(function (c, i) {
            var pts = CORNER.map(function (p) {
                return round(c.x - p[0] * e * c.d1[0] + p[1] * e * c.d2[0]) + " " +
                       round(c.y - p[0] * e * c.d1[1] + p[1] * e * c.d2[1]);
            });
            d += (i === 0 ? "M" : "L") + pts[0] +
                 "C" + pts.slice(1, 4).join(" ") +
                 "C" + pts.slice(4, 7).join(" ") +
                 "C" + pts.slice(7, 10).join(" ");
        });
        return d + "Z";
    }

    function draw(el, extent) {
        var w = el.offsetWidth, h = el.offsetHeight;
        if (!w || !h) return;
        var line = parseFloat(getComputedStyle(el).borderTopWidth) || 0;
        var svg = el.querySelector(":scope > .corner-stroke");
        if (!svg) {
            svg = document.createElementNS(SVG, "svg");
            svg.setAttribute("class", "corner-stroke");
            svg.setAttribute("aria-hidden", "true");
            svg.appendChild(document.createElementNS(SVG, "path"));
            el.insertBefore(svg, el.firstChild);
        }
        svg.setAttribute("viewBox", "0 0 " + w + " " + h);
        svg.style.width = w + "px";
        svg.style.height = h + "px";
        var path = svg.firstChild;
        path.setAttribute("d", outline(w, h, extent, line / 2));
        path.setAttribute("stroke-width", line);
        // A title set into the border sticks out above the card, so titled
        // cards keep their paper ground unclipped.
        if (!el.classList.contains("card--titled")) {
            el.style.clipPath = "path('" + outline(w, h, extent + line / 2, 0) + "')";
        }
        el.classList.add("has-continuous-corners");
    }

    function start() {
        if (!window.ResizeObserver) return;
        var extents = new Map();
        SHAPES.forEach(function (shape) {
            document.querySelectorAll(shape.selector).forEach(function (el) {
                if (!extents.has(el)) extents.set(el, shape.extent);
            });
        });
        var observer = new ResizeObserver(function (entries) {
            entries.forEach(function (entry) {
                draw(entry.target, extents.get(entry.target));
            });
        });
        extents.forEach(function (extent, el) {
            observer.observe(el);
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", start);
    } else {
        start();
    }
})();
