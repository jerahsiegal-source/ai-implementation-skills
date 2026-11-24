#!/usr/bin/env node
// Self-test for the /chart scripts. Needs Playwright for check-chart.mjs.
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));
const run = (script, argv) => { try { return { code: 0, out: execFileSync("node", [join(here, script), ...argv], { encoding: "utf8" }) }; } catch (e) { return { code: e.status, out: e.stdout || "" }; } };
let bad = 0;
const expect = (ok, msg) => { console.log(`${ok ? "pass" : "FAIL"}  ${msg}`); if (!ok) bad++; };

// Palette checker
expect(run("check-palette.mjs", ["#245080,#7E4D28,#0F835B,#840B47,#5F21B7,#A97D1B", "--bg", "#FFFFFF"]).code === 0, "default light palette passes on white");
expect(run("check-palette.mjs", ["#487ABB,#BC7F4F,#70EEB6,#E073B6,#A070DA,#DAC66E", "--bg", "#12181D"]).code === 0, "default dark palette passes on dark");
const rainbow = run("check-palette.mjs", ["#ff0000,#00ff00,#0000ff,#ffee00", "--bg", "#FFFFFF"]);
expect(rainbow.code === 1 && /mark-contrast/.test(rainbow.out), "bright rainbow fails contrast on white");
expect(/cvd-deutan/.test(run("check-palette.mjs", ["#5B9A3C,#C8553D", "--bg", "#FFFFFF"]).out), "red/green pair flagged for color blindness");

// Chart checker
const good = run("check-chart.mjs", [join(here, "../templates/charts.html")]);
expect(good.code === 0 && !/WARN/.test(good.out), "starter template passes with no warnings");
const badc = run("check-chart.mjs", [join(here, "fixtures/bad-charts.html")]);
expect(badc.code === 1, "bad charts page fails");
for (const id of ["takeaway", "text-path", "bar-baseline", "label-overlap", "label-clipped", "dual-axis", "pie-slices", "too-many-colors", "mark-effects", "rotated-labels", "tiny-chart-text", "mark-contrast", "label-on-line"])
  expect(new RegExp(`\\b${id}\\b`).test(badc.out), `bad charts page flags ${id}`);

console.log(bad ? `\n${bad} self-test checks failed.` : "\nAll self-test checks passed.");
process.exit(bad ? 1 : 0);
