#!/usr/bin/env node
// check-palette.mjs: will these chart colors work? Checks each color against the
// background and checks that every pair stays tellable apart for common color blindness.
//
// Usage:
//   node check-palette.mjs "#2B6CB0,#C05621,#2F855A" --bg "#FFFFFF" [--bg2 "#12181D"] [--json]
//   node check-palette.mjs --from DESIGN.md --bg "#F7F8F6"     (reads hex codes from a "Chart" line or section)
// Exit 0 = passes, 1 = a FAIL, 2 = bad input.

import { readFileSync } from "node:fs";

const args = process.argv.slice(2);
const opt = (n) => { const i = args.indexOf(n); return i > -1 ? args[i + 1] : undefined; };
const hexRe = /#[0-9a-f]{6}\b|#[0-9a-f]{3}\b/gi;

let colors = [];
if (opt("--from")) {
  const lines = readFileSync(opt("--from"), "utf8").split(/\r?\n/);
  const start = lines.findIndex((l) => /^#+\s*chart/i.test(l));
  let picked = [];
  if (start > -1) { for (let i = start + 1; i < lines.length && !/^#+\s/.test(lines[i]); i++) picked.push(lines[i]); }
  else picked = lines.filter((l) => /chart/i.test(l));
  colors = picked.join("\n").match(hexRe) || [];
} else {
  const list = args.find((a, i) => !a.startsWith("--") && !["--bg", "--bg2", "--from"].includes(args[i - 1]));
  colors = (list || "").match(hexRe) || [];
}
const bgs = [opt("--bg") || "#FFFFFF", opt("--bg2")].filter(Boolean);
if (colors.length < 1) { console.error('Give colors: node check-palette.mjs "#aaa,#bbb" --bg "#fff"'); process.exit(2); }

const norm = (h) => { h = h.replace("#", ""); if (h.length === 3) h = [...h].map((c) => c + c).join(""); return [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16)); };
const lin = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
const unlin = (v) => 255 * (v <= 0.0031308 ? 12.92 * v : 1.055 * v ** (1 / 2.4) - 0.055);
const lum = (rgb) => { const [r, g, b] = rgb.map(lin); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
const contrast = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
function lab(rgb) {
  const [r, g, b] = rgb.map(lin);
  let x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047, y = 0.2126 * r + 0.7152 * g + 0.0722 * b, z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883;
  const f = (t) => (t > 0.008856 ? Math.cbrt(t) : 7.787 * t + 16 / 116);
  [x, y, z] = [f(x), f(y), f(z)];
  return [116 * y - 16, 500 * (x - y), 200 * (y - z)];
}
const dE = (a, b) => Math.hypot(...lab(a).map((v, i) => v - lab(b)[i]));
// Machado et al. (2009) full-severity simulation matrices, applied in linear RGB.
const M = {
  protan: [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
  deutan: [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.01182, 0.04294, 0.968881]],
  tritan: [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.3039]],
};
const sim = (rgb, m) => { const l = rgb.map(lin); return m.map((row) => Math.min(255, Math.max(0, unlin(Math.min(1, Math.max(0, row[0] * l[0] + row[1] * l[1] + row[2] * l[2])))))); };

const res = [];
const add = (status, id, msg) => res.push({ status, id, msg });
const rgbs = colors.map(norm);

for (const bg of bgs) {
  const b = norm(bg);
  rgbs.forEach((c, i) => {
    const r = contrast(c, b);
    if (r < 3) add("fail", "mark-contrast", `${colors[i]} on ${bg} is ${r.toFixed(2)}:1. Chart marks need 3:1 to be seen.`);
  });
}
if (colors.length > 8) add("warn", "too-many", `${colors.length} colors. Past 6 to 8, readers can't match colors to a legend. Group the rest as "Other" or use small multiples.`);

const PAIR_MIN = 12, PAIR_MIN_CVD = 9;
for (let i = 0; i < rgbs.length; i++) for (let j = i + 1; j < rgbs.length; j++) {
  const d = dE(rgbs[i], rgbs[j]);
  if (d < PAIR_MIN) add("fail", "too-similar", `${colors[i]} and ${colors[j]} look almost the same (difference ${d.toFixed(1)}, need ${PAIR_MIN}).`);
  for (const [name, m] of Object.entries(M)) {
    const ds = dE(sim(rgbs[i], m), sim(rgbs[j], m));
    if (ds < PAIR_MIN_CVD && d >= PAIR_MIN) add(name === "tritan" ? "warn" : "fail", `cvd-${name}`, `${colors[i]} and ${colors[j]} blur together for ${name}opia (difference ${ds.toFixed(1)}, need ${PAIR_MIN_CVD}). Label lines directly or change one.`);
  }
}
const ls = rgbs.map((c) => lab(c)[0]);
if (rgbs.length >= 3 && Math.max(...ls) - Math.min(...ls) < 15) add("warn", "flat-lightness", `All colors have similar lightness (${Math.min(...ls).toFixed(0)} to ${Math.max(...ls).toFixed(0)}). In grayscale or for color-blind readers they will look alike.`);

const fails = res.filter((r) => r.status === "fail").length;
if (args.includes("--json")) console.log(JSON.stringify({ colors, backgrounds: bgs, results: res, failed: fails }, null, 2));
else {
  for (const r of res) console.log(`${r.status === "fail" ? "FAIL" : "WARN"} ${r.id.padEnd(15)} ${r.msg}`);
  console.log(`${colors.length} colors on ${bgs.join(" and ")}: ${fails} failed, ${res.length - fails} warnings.`);
}
process.exit(fails ? 1 : 0);
