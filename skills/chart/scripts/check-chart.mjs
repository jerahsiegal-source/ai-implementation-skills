#!/usr/bin/env node
// check-chart.mjs: chart-specific checks on an HTML page, on top of the design kit's check-page.mjs.
//
// Usage: node check-chart.mjs <page.html | url> [--json] [--allow id,id]
// Needs Playwright (same install as check-page.mjs). Exit 0 = no FAIL, 1 = FAIL, 2 = could not run.
//
// Charts made by the /chart skill wrap each chart in <figure data-chart="<form>"> and may declare
// data-y-min, data-series and data-y2. The checker also inspects the drawn SVG itself, so a chart
// without those attributes is still checked for overlap, clipping, text size, colors and a text path.

import { resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { createRequire } from "node:module";
import { readFileSync } from "node:fs";

const args = process.argv.slice(2);
const opt = (n) => { const i = args.indexOf(n); return i > -1 ? args[i + 1] : undefined; };
const target = args.find((a, i) => !a.startsWith("--") && args[i - 1] !== "--allow");
if (!target) { console.error("Usage: node check-chart.mjs <page.html | url> [--json] [--allow id,id]"); process.exit(2); }
const isUrl = /^https?:\/\//i.test(target);

let chromium = null;
try { chromium = createRequire(resolve("x.js"))("playwright").chromium; } catch {}
if (!chromium) try { chromium = (await import("playwright")).chromium; } catch {}
if (!chromium) {
  console.error("SKIP all chart checks: Playwright not installed (npm i -g playwright, then npx playwright install chromium).");
  process.exit(2);
}

const html = isUrl ? "" : readFileSync(resolve(target), "utf8");
const allowed = new Set([opt("--allow") || "", (html.match(/<meta[^>]+name=["']slop-ok["'][^>]+content=["']([^"']*)["']/i) || [])[1] || ""].join(",").split(",").map((s) => s.trim()).filter(Boolean));

const browser = await chromium.launch();
const results = [];
const add = (status, id, chart, msg) => results.push({ status: status !== "pass" && allowed.has(id) ? "allowed" : status, id, chart, msg });

for (const [vpName, vp] of [["desktop", { width: 1280, height: 860 }], ["phone", { width: 390, height: 844 }]]) {
  const page = await browser.newPage({ viewport: vp });
  await page.goto(isUrl ? target : pathToFileURL(resolve(target)).href, { waitUntil: "networkidle", timeout: 30000 });
  await page.waitForTimeout(500);
  const charts = await page.evaluate(() => {
    const out = [];
    // Any CSS color (rgb, color(srgb ...), oklch, color-mix results) -> [r, g, b, a] in 0-255, via a canvas pixel.
        const _cv = document.createElement("canvas"); _cv.width = _cv.height = 1; const _cx = _cv.getContext("2d", { willReadFrequently: true });
        const parse = (c) => { if (!c || c === "none" || c === "transparent") return null; if (/^rgba?\(/.test(c)) { const m = c.match(/[\d.]+/g); return m.map(Number); } _cx.clearRect(0, 0, 1, 1); _cx.fillStyle = "#000"; _cx.fillStyle = c; _cx.fillRect(0, 0, 1, 1); const d = _cx.getImageData(0, 0, 1, 1).data; return [d[0], d[1], d[2], d[3] / 255]; };
    const lum = ([r, g, b]) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
    const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
    const bgOf = (el) => { for (let e = el; e; e = e.parentElement) { const c = parse(getComputedStyle(e).backgroundColor); if (c && (c.length < 4 || c[3] > 0.5)) return c; } return [255, 255, 255]; };
    const graphics = [...document.querySelectorAll("svg, canvas")].filter((g) => {
      const r = g.getBoundingClientRect();
      return r.width >= 120 && r.height >= 80 && !g.closest("button, a, nav");
    });
    graphics.forEach((g, idx) => {
      const fig = g.closest("figure") || g.parentElement;
      const name = fig.getAttribute("data-chart-name") || fig.querySelector("figcaption, h2, h3, h4")?.textContent.trim().slice(0, 40) || `${g.tagName.toLowerCase()} #${idx + 1}`;
      const d = { name, kind: g.tagName.toLowerCase(), form: fig.getAttribute("data-chart") || "", yMin: fig.getAttribute("data-y-min"), y2: fig.hasAttribute("data-y2"), series: fig.getAttribute("data-series") };
      // A text path: a caption or heading that states the chart, and a data table or a text summary.
      const caption = fig.querySelector("figcaption, h2, h3, h4, [data-takeaway]")?.textContent.trim() || "";
      d.hasTitle = caption.length > 3;
      d.hasTable = !!fig.querySelector("table") || !!fig.parentElement?.querySelector(":scope > details table");
      d.hasLabel = (g.getAttribute("role") === "img" && !!(g.getAttribute("aria-label") || g.getAttribute("aria-labelledby"))) || !!g.querySelector(":scope > title, :scope > desc") || (g.tagName === "CANVAS" && !!g.textContent.trim());
      if (g.tagName === "CANVAS") { out.push(d); return; }
      const box = g.getBoundingClientRect();
      const texts = [...g.querySelectorAll("text")].filter((t) => t.textContent.trim() && getComputedStyle(t).display !== "none" && getComputedStyle(t).visibility !== "hidden" && t.getBoundingClientRect().width > 0);
      const rects = texts.map((t) => ({ t: t.textContent.trim().slice(0, 20), r: t.getBoundingClientRect(), size: parseFloat(getComputedStyle(t).fontSize), rot: /rotate\((?!0\b)/.test(t.getAttribute("transform") || "") || /rotate\((?!0)/.test(getComputedStyle(t).transform === "none" ? "" : t.getAttribute("transform") || "") }));
      let overlaps = [];
      for (let i = 0; i < rects.length; i++) for (let j = i + 1; j < rects.length; j++) {
        const a = rects[i].r, b = rects[j].r;
        const w = Math.min(a.right, b.right) - Math.max(a.left, b.left), h = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
        if (w > 1 && h > 1 && (w * h) / Math.min(a.width * a.height, b.width * b.height) > 0.2) overlaps.push(`"${rects[i].t}" / "${rects[j].t}"`);
      }
      d.overlaps = overlaps;
      // Labels crossed by a reference line (dashed lines: targets, averages).
      const refs = [...g.querySelectorAll("line, path, polyline")].filter((l) => (getComputedStyle(l).strokeDasharray || "none") !== "none").map((l) => l.getBoundingClientRect());
      d.onLine = rects.filter(({ r }) => refs.some((b) => {
        const w = Math.min(r.right, b.right) - Math.max(r.left, b.left), h = Math.min(r.bottom, b.bottom) - Math.max(r.top, b.top);
        return w >= -0.5 && h > 2 && b.left > r.left + 2 && b.right < r.right - 2;
      })).map((x) => x.t);
      d.clipped = rects.filter(({ r }) => r.left < box.left - 1 || r.right > box.right + 1 || r.top < box.top - 1 || r.bottom > box.bottom + 1).map((x) => x.t);
      d.tiny = rects.filter((x) => x.size < 11).length;
      d.rotated = rects.filter((x) => x.rot).length;
      d.textCount = rects.length;
      // Marks: filled or stroked shapes that are not thin gray gridlines.
      const marks = [...g.querySelectorAll("rect, path, circle, ellipse, polygon, polyline, line")].filter((m) => {
        const r = m.getBoundingClientRect(); if (r.width * r.height === 0 && !(r.width > 4 || r.height > 4)) return false;
        return !m.closest("defs, clipPath, mask, marker");
      });
      const markColors = new Map();
      let lowMarks = new Set();
      const bg = bgOf(g);
      for (const m of marks) {
        const cs = getComputedStyle(m);
        for (const c of [cs.fill, cs.stroke]) {
          const p = parse(c);
          if (!p || c === "none" || (p.length > 3 && p[3] < 0.3)) continue;
          const spread = Math.max(p[0], p[1], p[2]) - Math.min(p[0], p[1], p[2]);
          if (spread < 32) continue; // grays: axes, gridlines, quiet context marks
          const key = `rgb(${p[0]},${p[1]},${p[2]})`;
          markColors.set(key, (markColors.get(key) || 0) + 1);
          if (ratio(p, bg) < 3) lowMarks.add(key);
        }
      }
      d.colors = markColors.size;
      d.lowMarks = [...lowMarks].slice(0, 3);
      d.shadow = marks.some((m) => /drop-shadow|blur/.test(getComputedStyle(m).filter || "")) || !!g.querySelector("filter feDropShadow, filter feGaussianBlur");
      d.gradientMarks = marks.some((m) => /url\(/.test(getComputedStyle(m).fill || ""));
      d.slices = d.form.match(/pie|donut/) ? Number(d.series || g.querySelectorAll("path").length) : 0;
      out.push(d);
    });
    return out;
  });
  await page.close();

  if (vpName === "desktop") {
    if (!charts.length) add("skipped", "no-charts", "-", "No SVG or canvas charts found on the page.");
    for (const c of charts) {
      const n = c.name;
      add(c.hasTitle ? "pass" : "fail", "takeaway", n, c.hasTitle ? "" : "Chart has no title or takeaway text next to it. State what the reader should see.");
      add(c.hasTable || c.hasLabel ? "pass" : "fail", "text-path", n, c.hasTable || c.hasLabel ? "" : 'No way to get the numbers without seeing the chart. Add a data table (for example behind "Show data") or role="img" with an aria-label that states the takeaway.');
      if (c.kind === "canvas") { add("skipped", "canvas", n, "Canvas chart: label overlap, clipping and color checks can't see inside it. Prefer SVG, and include a data table."); continue; }
      if (/bar|column|histogram/.test(c.form) && c.yMin !== null && Number(c.yMin) !== 0) add("fail", "bar-baseline", n, `Bar chart axis starts at ${c.yMin}, not 0. Bars must start at zero, or use dots instead.`);
      if (c.y2) add("warn", "dual-axis", n, "Two y-axes. Readers compare the lines as if they shared a scale. Use two charts side by side instead.");
      if (c.slices > 5) add("warn", "pie-slices", n, `${c.slices} slices. Past 5, use a bar chart sorted by size.`);
      if (c.colors > 7) add("warn", "too-many-colors", n, `${c.colors} mark colors. Highlight what matters in color and put the rest in gray, or split into small multiples.`);
      if (c.lowMarks.length) add("fail", "mark-contrast", n, `Marks under 3:1 contrast with the background: ${c.lowMarks.join(", ")}.`);
      if (c.shadow) add("warn", "mark-effects", n, "Shadows or blur on chart marks. They add noise and blur the values.");
      if (c.gradientMarks) add("warn", "gradient-marks", n, "Gradient fills on marks make values harder to read. Use flat color.");
      if (c.rotated) add("warn", "rotated-labels", n, `${c.rotated} rotated labels. Flip to a horizontal bar chart or shorten the labels.`);
    }
  }
  for (const c of charts.filter((x) => x.kind === "svg")) {
    if (c.overlaps.length) add("fail", "label-overlap", `${c.name} (${vpName})`, `${c.overlaps.length} labels overlap, e.g. ${c.overlaps.slice(0, 2).join(", ")}.`);
    if (c.clipped.length) add("fail", "label-clipped", `${c.name} (${vpName})`, `${c.clipped.length} labels are cut off at the chart edge, e.g. "${c.clipped[0]}". Leave room in the viewBox.`);
    if (c.onLine.length) add("warn", "label-on-line", `${c.name} (${vpName})`, `A reference line runs through ${c.onLine.length} labels, e.g. "${c.onLine[0]}". Move the label or put it inside the bar.`);
    if (c.tiny) add("warn", "tiny-chart-text", `${c.name} (${vpName})`, `${c.tiny} chart labels are under 11px.`);
  }
}
await browser.close();

const shown = results.filter((r) => r.status !== "pass");
const fails = results.filter((r) => r.status === "fail").length;
if (args.includes("--json")) console.log(JSON.stringify({ target, failed: fails, results: shown }, null, 2));
else {
  const label = { fail: "FAIL", warn: "WARN", skipped: "SKIP", allowed: "OK* " };
  for (const s of ["fail", "warn", "allowed", "skipped"]) for (const r of shown.filter((x) => x.status === s)) console.log(`${label[s]} ${r.id.padEnd(17)} [${r.chart}] ${r.msg}`);
  const charts = new Set(results.map((r) => r.chart.replace(/ \((desktop|phone)\)$/, ""))).size;
  console.log(`${charts} charts checked: ${fails} failed, ${shown.filter((r) => r.status === "warn").length} warnings, ${shown.filter((r) => r.status === "skipped").length} skipped.`);
}
process.exit(fails ? 1 : 0);
