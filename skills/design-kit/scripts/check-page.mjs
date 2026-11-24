#!/usr/bin/env node
// check-page.mjs: catch AI slop and broken layout in an HTML page before handing it back.
//
// Usage:
//   node check-page.mjs <file.html | http(s)://url> [--out <dir>] [--json] [--allow id,id] [--static]
//
// Static checks need only Node 18+. Render checks (screenshots, overflow, contrast,
// tiny text, console errors) need Playwright; without it they are reported as skipped.
// Exit code: 0 = no failures, 1 = at least one FAIL, 2 = could not read the page.
//
// To accept a pattern the user or brand asked for, pass --allow <id> or put
// <meta name="slop-ok" content="id,id"> in the page. Every result line shows its id.

import { readFileSync, mkdirSync } from "node:fs";
import { resolve, join, basename } from "node:path";
import { pathToFileURL } from "node:url";
import { createRequire } from "node:module";

const args = process.argv.slice(2);
const flag = (name) => args.includes(name);
const opt = (name, dflt) => {
  const i = args.indexOf(name);
  return i > -1 && args[i + 1] ? args[i + 1] : dflt;
};
const target = args.find((a, i) => !a.startsWith("--") && !["--out", "--allow"].includes(args[i - 1]));
if (!target) {
  console.error("Usage: node check-page.mjs <file.html | url> [--out dir] [--json] [--allow id,id] [--static]");
  process.exit(2);
}
const isUrl = /^https?:\/\//i.test(target);
const outDir = resolve(opt("--out", "check-shots"));

const results = [];
const add = (status, id, msg) => results.push({ status, id, msg });

// ---------- load ----------
let html = "";
try {
  html = isUrl ? await (await fetch(target)).text() : readFileSync(resolve(target), "utf8");
} catch (e) {
  console.error(`Could not read ${target}: ${e.message}`);
  process.exit(2);
}

const allowed = new Set(
  [opt("--allow", ""), (html.match(/<meta[^>]+name=["']slop-ok["'][^>]+content=["']([^"']*)["']/i) || [])[1] || ""]
    .join(",").split(",").map((s) => s.trim()).filter(Boolean)
);

// ---------- helpers ----------
const css = [...html.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/gi)].map((m) => m[1]).join("\n")
  + "\n" + [...html.matchAll(/style=["']([^"']*)["']/gi)].map((m) => m[1]).join(";\n");
const body = html.replace(/<script[\s\S]*?<\/script>/gi, " ").replace(/<style[\s\S]*?<\/style>/gi, " ");
const decode = (s) => s.replace(/&nbsp;/g, " ").replace(/&amp;/g, "&").replace(/&mdash;/g, "—").replace(/&rarr;/g, "→")
  .replace(/&#8212;/g, "—").replace(/&#x2014;/gi, "—").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'");
const textOf = (s) => decode(s.replace(/<[^>]+>/g, " ")).replace(/\s+/g, " ").trim();
const visible = textOf(body);
const tagTexts = (tags) => [...body.matchAll(new RegExp(`<(${tags})\\b[^>]*>([\\s\\S]*?)<\\/\\1>`, "gi"))].map((m) => ({ tag: m[1].toLowerCase(), text: textOf(m[2]) }));
const words = (s) => s.split(/\s+/).filter(Boolean).length;
const short = (s, n = 70) => (s.length > n ? s.slice(0, n - 1) + "…" : s);

function hexToHsl(hex) {
  let h = hex.replace("#", "");
  if (h.length === 3) h = h.split("").map((c) => c + c).join("");
  if (h.length !== 6) return null;
  const [r, g, b] = [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16) / 255);
  const max = Math.max(r, g, b), min = Math.min(r, g, b), l = (max + min) / 2;
  if (max === min) return { h: 0, s: 0, l };
  const d = max - min, s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
  let hue = max === r ? (g - b) / d + (g < b ? 6 : 0) : max === g ? (b - r) / d + 2 : (r - g) / d + 4;
  return { h: hue * 60, s, l };
}
const hexes = (s) => (s.match(/#[0-9a-f]{6}\b|#[0-9a-f]{3}\b/gi) || []).map(hexToHsl).filter(Boolean);

// A check either passes or records a FAIL / WARN. Allowed ids become "allowed".
function check(id, level, failed, msg) {
  if (!failed) return add("pass", id, msg.pass || "ok");
  if (allowed.has(id)) return add("allowed", id, msg.fail + " (allowed)");
  add(level, id, msg.fail);
}

// ---------- static: visual slop ----------
const gradients = css.match(/linear-gradient\([^;]*\)/gi) || [];
const purpleBlue = gradients.some((g) => {
  const hs = hexes(g).filter((c) => c.s > 0.35).map((c) => c.h);
  return hs.some((h) => h >= 255 && h <= 300) && hs.some((h) => h >= 195 && h < 255);
});
check("gradient-hero", "fail", purpleBlue, { fail: "Purple-to-blue gradient found. This is the most common AI look." });

const colors = hexes(css);
const cream = colors.some((c) => c.l > 0.88 && c.l < 0.97 && c.h >= 30 && c.h <= 55 && c.s > 0.15);
const terracotta = colors.some((c) => c.h >= 8 && c.h <= 25 && c.s > 0.4 && c.l > 0.4 && c.l < 0.65);
check("cream-terracotta", "fail", cream && terracotta, { fail: "Cream background plus terracotta accent: a stock AI palette." });

const darkBg = colors.some((c) => c.l < 0.09);
const neon = colors.filter((c) => c.s > 0.85 && c.l > 0.45 && ((c.h >= 70 && c.h <= 140) || (c.h >= 10 && c.h <= 30)));
check("neon-on-black", "warn", darkBg && neon.length > 0 && colors.filter((c) => c.s > 0.3).length <= 3,
  { fail: "Near-black with one acid green or orange accent: a stock AI look. Fine only if it was chosen." });

const emojiRe = /\p{Extended_Pictographic}/u;
const headings = tagTexts("h1|h2|h3|h4|summary|button|li|th");
const emojiHeads = headings.filter((h) => emojiRe.test(h.text) && !/^[✓✗✔✘★☆]/.test(h.text));
check("emoji-icons", "fail", emojiHeads.length >= 2, { fail: `Emoji used as icons in ${emojiHeads.length} headings or items, e.g. "${short(emojiHeads[0]?.text || "")}".` });

const leftBars = (css.match(/border-left\s*:\s*[3-9]px\s+solid/gi) || []).length;
check("accent-bar-cards", "warn", leftBars >= 3, { fail: `${leftBars} rules put a thick colored bar on the left of a block. One is a choice; many is a template.` });

const glass = (css.match(/backdrop-filter\s*:\s*blur/gi) || []).length;
const glow = (css.match(/box-shadow\s*:[^;]*0\s+0\s+(?:[2-9]\d|1\d\d)px/gi) || []).length;
check("glass-glow", "warn", glass + glow >= 2, { fail: `Glass blur or glow used ${glass + glow} times. Keep effects only where they mean something.` });

const radii = (css.match(/border-radius\s*:\s*[^;}]+/gi) || []).map((r) => r.replace(/\s/g, ""));
const radCount = radii.reduce((m, r) => ((m[r] = (m[r] || 0) + 1), m), {});
const topRad = Object.entries(radCount).sort((a, b) => b[1] - a[1])[0];
const shadows = (css.match(/box-shadow\s*:/gi) || []).length;
check("same-card-everywhere", "warn", topRad && topRad[1] >= 8 && shadows >= 6,
  { fail: `The same radius (${topRad?.[0]}) is used ${topRad?.[1]} times with ${shadows} shadows: every block looks like the same card.` });

const fontDecl = (css.match(/font-family\s*:\s*([^;}]+)/gi) || []).join(" ");
const families = new Set((fontDecl.match(/["']?([A-Z][\w ]+?)["']?(?=\s*[,;)]|$)/g) || []).map((f) => f.replace(/["']/g, "").trim()));
const onlyInter = /Inter\b/.test(fontDecl) && ![...families].some((f) => f && !/^(Inter|system-ui|sans-serif|serif|monospace|Segoe UI|Roboto|Arial|Helvetica|Consolas|Menlo|ui-monospace|SF Mono|Cascadia Code|Helvetica Neue|BlinkMacSystemFont|Apple Color Emoji)$/i.test(f));
check("default-type", "warn", onlyInter, { fail: "Inter is the only typeface. Pair a display face with the body face, or say why Inter fits." });

// ---------- static: wording slop ----------
const lorem = /lorem ipsum|dolor sit amet/i.test(visible);
check("placeholder", "fail", lorem, { fail: "Placeholder text (lorem ipsum) is still on the page." });

const emDashes = (visible.match(/—/g) || []).length;
check("em-dashes", "warn", emDashes > 2, { fail: `${emDashes} em-dashes in the text. Use short sentences or commas instead.` });

const notBut = visible.match(/\b(?:isn['’]t just|is not just|not just [^.]{1,40}, but|it['’]s not [^.]{1,40}[,;—] it['’]s|not [^.,]{1,30}, but [^.,]{1,30})/gi) || [];
check("not-x-but-y", "warn", notBut.length > 0, { fail: `"Not X, but Y" framing: "${short(notBut[0] || "")}".` });

const stock = visible.match(/\b(delve|seamless(?:ly)?|unlock(?:s|ing)? the|elevate your|game[- ]changer|in today['’]s|worth noting|honest caveat|let['’]s dive|supercharge|effortless(?:ly)?|robust and scalable|at the end of the day|look no further|harness the power)\b/gi) || [];
check("stock-phrases", "warn", stock.length > 0, { fail: `Stock AI phrases: ${[...new Set(stock.map((s) => s.toLowerCase()))].join(", ")}.` });

const h1s = tagTexts("h1"), h2s = tagTexts("h2|h3");
const longH1 = h1s.filter((h) => words(h.text) > 8);
const longH2 = h2s.filter((h) => words(h.text) > 10);
check("long-titles", "warn", longH1.length + longH2.length > 0,
  { fail: `Titles that read like descriptions (${longH1.length + longH2.length}), e.g. "${short((longH1[0] || longH2[0])?.text || "")}". A title names the thing in a few words.` });

const titleTag = (html.match(/<title>([\s\S]*?)<\/title>/i) || [])[1] || "";
check("page-title", "warn", !titleTag.trim() || words(textOf(titleTag)) > 6 || /\s[-–—:]\s/.test(titleTag),
  { fail: titleTag.trim() ? `Page title "${short(textOf(titleTag))}" is long or has an explainer after a dash or colon.` : "No <title>." });

// A caption/subtitle that mostly repeats its heading.
let restated = 0;
for (const m of body.matchAll(/<(h[1-3])\b[^>]*>([\s\S]*?)<\/\1>\s*<(p|small|span|div)\b[^>]*>([\s\S]*?)<\/\3>/gi)) {
  const hw = new Set(textOf(m[2]).toLowerCase().match(/[a-z]{4,}/g) || []);
  const cw = textOf(m[4]).toLowerCase().match(/[a-z]{4,}/g) || [];
  if (hw.size >= 2 && cw.length && cw.filter((w) => hw.has(w)).length / hw.size >= 0.75) restated++;
}
check("caption-restates", "warn", restated >= 2, { fail: `${restated} captions mostly repeat their heading. Cut them or say something new.` });

const numbered = (body.match(/>\s*0[1-9]\s*[.\/]?\s*</g) || []).length;
check("fake-numbering", "warn", numbered >= 3, { fail: `${numbered} decorative 01 / 02 / 03 markers. Use numbers only for a real sequence.` });

const caps = (css.match(/text-transform\s*:\s*uppercase/gi) || []).length;
check("caps-labels", "warn", caps >= 4, { fail: `${caps} all-caps label styles. One kind of small caps label is plenty.` });

const arrowLinks = [...body.matchAll(/<a\b[^>]*>([\s\S]*?)<\/a>/gi)].filter((m) => /→|&rarr;/.test(m[1])).length;
check("arrow-links", "warn", arrowLinks >= 3, { fail: `${arrowLinks} links end in "→". Let the link text do the work.` });

const dots = (visible.match(/\w+ · \w+ · \w+/g) || []).length;
check("dot-metadata", "warn", dots >= 3, { fail: `${dots} "A · B · C" metadata lines. A stock AI layout habit.` });

// ---------- render checks ----------
const renderIds = ["screenshots", "phone-overflow", "contrast", "tiny-text", "all-centered", "clipped-text", "console-errors", "img-alt", "dark-mode"];
let chromium = null;
if (!flag("--static")) {
  for (const base of [process.cwd(), resolve(".")]) {
    try { chromium = createRequire(join(base, "x.js"))("playwright").chromium; break; } catch {}
  }
  if (!chromium) try { chromium = (await import("playwright")).chromium; } catch {}
}

if (!chromium) {
  for (const id of renderIds) add("skipped", id, flag("--static") ? "--static given" : "Playwright not installed (npm i -g playwright, then npx playwright install chromium)");
} else {
  const url = isUrl ? target : pathToFileURL(resolve(target)).href;
  const browser = await chromium.launch();
  mkdirSync(outDir, { recursive: true });
  const stem = basename(isUrl ? new URL(target).hostname : target).replace(/\.[^.]+$/, "");
  const shots = [];
  const errors = [];
  const metrics = {};
  for (const [name, vp] of [["desktop", { width: 1280, height: 860 }], ["phone", { width: 390, height: 844 }]]) {
    for (const scheme of ["light", "dark"]) {
      const page = await browser.newPage({ viewport: vp, colorScheme: scheme });
      page.on("console", (m) => m.type() === "error" && errors.push(m.text()));
      page.on("pageerror", (e) => errors.push(String(e.message || e)));
      await page.goto(url, { waitUntil: "networkidle", timeout: 30000 }).catch((e) => errors.push("load: " + e.message));
      await page.waitForTimeout(400);
      const file = join(outDir, `${stem}-${name}-${scheme}.png`);
      await page.screenshot({ path: file, fullPage: true });
      shots.push(file);
      // Open every "Show data" and other <details>, so hidden tables count for sideways scroll.
      await page.evaluate(() => document.querySelectorAll("details:not([open])").forEach((d) => d.setAttribute("open", ""))).catch(() => {});
      await page.waitForTimeout(150);
      metrics[`${name}-${scheme}`] = await page.evaluate(() => {
        // Any CSS color (rgb, color(srgb ...), oklch, color-mix results) -> [r, g, b, a] in 0-255, via a canvas pixel.
        const _cv = document.createElement("canvas"); _cv.width = _cv.height = 1; const _cx = _cv.getContext("2d", { willReadFrequently: true });
        const parse = (c) => { if (!c || c === "none" || c === "transparent") return [0, 0, 0, 0]; if (/^rgba?\(/.test(c)) { const m = c.match(/[\d.]+/g); return m.map(Number); } _cx.clearRect(0, 0, 1, 1); _cx.fillStyle = "#000"; _cx.fillStyle = c; _cx.fillRect(0, 0, 1, 1); const d = _cx.getImageData(0, 0, 1, 1).data; return [d[0], d[1], d[2], d[3] / 255]; };
        const lum = ([r, g, b]) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
        const bgOf = (el) => { for (let e = el; e; e = e.parentElement) { const st = getComputedStyle(e); if (st.backgroundImage !== "none") return null; const c = parse(st.backgroundColor); if (c.length < 4 || c[3] > 0.5) return c; } return [255, 255, 255]; };
        const els = [...document.body.querySelectorAll("*")].filter((el) => {
          const own = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim().length > 1);
          const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
          return own && r.width > 0 && r.height > 0 && cs.visibility !== "hidden" && cs.opacity !== "0";
        });
        let low = [], tiny = 0, centered = 0, blocks = 0, clipped = 0;
        for (const el of els) {
          const cs = getComputedStyle(el); const size = parseFloat(cs.fontSize); const bold = parseInt(cs.fontWeight) >= 700;
          const bg = bgOf(el); const a = lum(parse(cs.color)), b = bg ? lum(bg) : a; const ratio = !bg ? 99 : (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
          const need = size >= 24 || (size >= 18.6 && bold) ? 3 : 4.5;
          if (ratio < need) low.push(`${el.tagName.toLowerCase()} "${el.textContent.trim().slice(0, 30)}" ${ratio.toFixed(2)}:1`);
          if (size < 12) tiny++;
          if (/^(P|LI|H[1-6]|DIV|SPAN|TD)$/.test(el.tagName) && el.textContent.trim().length > 20) { blocks++; if (cs.textAlign === "center") centered++; }
          if ((cs.overflow === "hidden" || cs.textOverflow === "ellipsis") && el.scrollWidth > el.clientWidth + 2) clipped++;
        }
        // How many elements actually use all-caps labels or a thick colored left bar.
        let capsEls = 0, barEls = 0;
        for (const el of document.body.querySelectorAll("*")) {
          const cs = getComputedStyle(el); const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue;
          if (cs.textTransform === "uppercase" && el.textContent.trim().length > 2 && [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())) capsEls++;
          const bl = parseFloat(cs.borderLeftWidth), br = parseFloat(cs.borderRightWidth), c = parse(cs.borderLeftColor);
          if (bl >= 3 && br <= 1 && r.height > 30 && Math.max(c[0], c[1], c[2]) - Math.min(c[0], c[1], c[2]) > 40) barEls++;
        }
        const pageBg = (() => { for (const e of [document.body, document.documentElement]) { const c = parse(getComputedStyle(e).backgroundColor); if ((c[3] ?? 1) > 0.5) return lum(c); } return 1; })();
        return {
          capsEls, barEls, pageBg,
          overflow: document.documentElement.scrollWidth - window.innerWidth,
          low, tiny, centered, blocks, clipped,
          noAlt: [...document.images].filter((i) => !i.hasAttribute("alt")).length,
        };
      });
      await page.close();
    }
  }
  await browser.close();

  add("pass", "screenshots", `Saved ${shots.length}: ${shots.map((s) => basename(s)).join(", ")} in ${outDir}`);
  const ph = Math.max(metrics["phone-light"].overflow, metrics["phone-dark"].overflow);
  check("phone-overflow", "fail", ph > 1, { fail: `The page scrolls sideways on a phone by ${ph}px (with every <details> section open).` });
  const lowAll = [...new Set([...metrics["desktop-light"].low.map((l) => "light: " + l), ...metrics["desktop-dark"].low.map((l) => "dark: " + l)])];
  check("contrast", "fail", lowAll.length > 0, { fail: `${lowAll.length} text items are hard to read (low contrast), e.g. ${lowAll.slice(0, 3).join("; ")}.` });
  const tiny = metrics["phone-light"].tiny;
  check("tiny-text", "warn", tiny > 0, { fail: `${tiny} text items are smaller than 12px.` });
  const d = metrics["desktop-light"];
  check("all-centered", "warn", d.blocks >= 8 && d.centered / d.blocks > 0.6, { fail: `${Math.round((100 * d.centered) / d.blocks)}% of text blocks are centered. Left-align running text.` });
  const clip = Math.max(d.clipped, metrics["phone-light"].clipped);
  check("clipped-text", "warn", clip > 0, { fail: `${clip} text items are cut off.` });
  const errs = [...new Set(errors)];
  check("console-errors", "fail", errs.length > 0, { fail: `${errs.length} console errors, e.g. ${short(errs[0] || "", 120)}` });
  // Usage-based versions of two static checks: a single CSS rule can style many elements.
  const upgrade = (id, n, min, msg) => {
    const r = results.find((x) => x.id === id);
    if (r && r.status === "pass" && n >= min) { r.status = allowed.has(id) ? "allowed" : "warn"; r.msg = msg + (allowed.has(id) ? " (allowed)" : ""); }
  };
  upgrade("caps-labels", d.capsEls, 4, `${d.capsEls} all-caps labels on the page. Use sentence case; keep caps for at most one tiny label style.`);
  upgrade("accent-bar-cards", d.barEls, 2, `${d.barEls} blocks have a thick colored bar down the left side. A stock AI card style.`);
  const dk = metrics["desktop-dark"];
  check("dark-mode", "warn", d.pageBg > 0.6 && dk.pageBg > 0.6, { fail: "The page stays light when the reader's device is in dark mode. Add a prefers-color-scheme: dark theme, or allow this check if the brand is light only." });
  const noAlt = d.noAlt;
  check("img-alt", "warn", noAlt > 0, { fail: `${noAlt} images have no alt text.` });
}

// ---------- report ----------
const count = (s) => results.filter((r) => r.status === s).length;
const summary = { ran: results.length - count("skipped"), failed: count("fail"), warned: count("warn"), allowed: count("allowed"), skipped: count("skipped") };
if (flag("--json")) {
  console.log(JSON.stringify({ target, summary, results }, null, 2));
} else {
  const label = { fail: "FAIL", warn: "WARN", skipped: "SKIP", allowed: "OK* ", pass: "ok  " };
  for (const s of ["fail", "warn", "allowed", "skipped"]) for (const r of results.filter((x) => x.status === s)) console.log(`${label[s]} ${r.id.padEnd(20)} ${r.msg}`);
  const shotLine = results.find((r) => r.id === "screenshots" && r.status === "pass");
  if (shotLine) console.log(`ok   screenshots          ${shotLine.msg}`);
  console.log(`\n${summary.ran} checks ran: ${summary.failed} failed, ${summary.warned} warnings, ${summary.allowed} allowed, ${summary.skipped} skipped.`);
}
process.exit(summary.failed ? 1 : 0);
