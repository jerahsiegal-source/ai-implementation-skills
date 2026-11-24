#!/usr/bin/env node
// Self-test for check-page.mjs: the clean page must pass, the slop page must be caught.
// Run: node test-check-page.mjs   (add --static to skip browser checks)
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { tmpdir } from "node:os";

const here = dirname(fileURLToPath(import.meta.url));
const extra = process.argv.includes("--static") ? ["--static"] : [];
const run = (file, more = []) => {
  try {
    return { code: 0, out: JSON.parse(execFileSync("node", [join(here, "check-page.mjs"), join(here, "fixtures", file), "--json", "--out", join(tmpdir(), "check-page-test"), ...extra, ...more], { encoding: "utf8" })) };
  } catch (e) {
    return { code: e.status, out: JSON.parse(e.stdout) };
  }
};
const ids = (r, s) => r.out.results.filter((x) => x.status === s).map((x) => x.id);

let bad = 0;
const expect = (ok, msg) => { console.log(`${ok ? "pass" : "FAIL"}  ${msg}`); if (!ok) bad++; };

const clean = run("clean.html");
expect(clean.code === 0, "clean page exits 0");
expect(ids(clean, "warn").length === 0, `clean page has no warnings (${ids(clean, "warn").join(", ") || "none"})`);

const modern = run("modern-color.html");
if (!extra.length) expect(modern.code === 0 && !ids(modern, "fail").includes("contrast"), "color-mix() and oklch() colors are read correctly (no false contrast FAIL)");

const slop = run("slop.html");
expect(slop.code === 1, "slop page exits 1");
const mustFail = ["gradient-hero", "emoji-icons", "placeholder"];
const mustWarn = ["em-dashes", "not-x-but-y", "stock-phrases", "long-titles", "page-title", "fake-numbering", "caps-labels", "arrow-links", "accent-bar-cards", "same-card-everywhere", "default-type"];
if (!extra.length) mustFail.push("phone-overflow", "contrast");
for (const id of mustFail) expect(ids(slop, "fail").includes(id), `slop page fails ${id}`);
for (const id of mustWarn) expect(ids(slop, "warn").includes(id), `slop page warns ${id}`);

const allowed = run("slop.html", ["--allow", "gradient-hero,emoji-icons"]);
expect(ids(allowed, "allowed").includes("gradient-hero") && !ids(allowed, "fail").includes("gradient-hero"), "--allow turns a FAIL into allowed");

console.log(bad ? `\n${bad} self-test checks failed.` : "\nAll self-test checks passed.");
process.exit(bad ? 1 : 0);
