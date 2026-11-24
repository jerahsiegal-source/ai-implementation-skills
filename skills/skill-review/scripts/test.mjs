// Self-test for scan, record and dashboard, on the fixtures in ./fixtures. No network, no browser.
//   node skills/skill-review/scripts/test.mjs
import { execFileSync } from "node:child_process";
import { mkdtempSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { analyze, mergeUses, render } from "./dashboard.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const fx = join(here, "fixtures");
const tmp = mkdtempSync(join(tmpdir(), "skill-health-"));
let bad = 0;
const ok = (cond, msg) => { console.log(`${cond ? "ok  " : "FAIL"} ${msg}`); if (!cond) bad++; };
const node = (args) => execFileSync("node", args, { encoding: "utf8" });

// scan: Claude Code + Codex history -> uses
node([join(here, "scan.mjs"), "--claude-dir", join(fx, "claude"), "--codex-dir", join(fx, "codex"), "--out", join(tmp, "auto.jsonl"), "--skills", "design,visualize,chart,explore"]);
const uses = readFileSync(join(tmp, "auto.jsonl"), "utf8").trim().split("\n").map((l) => JSON.parse(l));
const by = (s) => uses.find((u) => u.skills.includes(s));
ok(uses.length === 4, `scan finds 4 skill uses (got ${uses.length})`);
ok(by("design")?.first_try === false && by("design").source === "rated" && by("design").note === "header too big", "/rate n in the transcript marks /design as a miss, with the note");
ok(by("design")?.fixes === 1 && by("design").model === "claude-opus-5-5", "/design: 1 fix round, model read from the reply");
ok(by("visualize")?.first_try === true && by("visualize").source === "guess", "/visualize with a thank-you follow-up counts as right first try (guessed)");
ok(by("chart")?.first_try === true, "a skill Claude called itself (Skill tool) is counted");
ok(by("explore")?.tool === "codex" && by("explore").fixes === 2 && by("explore").first_try === false && by("explore").model === "gpt-5.5-codex", "Codex $explore with two redo asks is a miss");
ok(!uses.some((u) => u.skills.includes("rate")), "/rate itself is never counted as a skill use");

// record: combo-kit run -> history entry, both judge orders
node([join(here, "record.mjs"), join(fx, "runs"), "--model", "test-model", "--date", "2026-11-24", "--blind2", join(fx, "runs", "blind-2"), "--out", tmp]);
const h = JSON.parse(readFileSync(join(tmp, "2026-11-24-test-model-claude-code.json"), "utf8"));
const arm = (id) => h.scenarios[0].arms.find((a) => a.arm === id);
ok(arm("chart").vsNone.result === "win" && arm("chart").vsNone.holds === false, "a win that flips to a tie in the second order does not hold");
ok(arm("chart+visualize").vsNone.holds === true && arm("chart+visualize").tokens === 100000 && arm("chart+visualize").fail === 0, "stack win holds both ways; cost and checker counts carried over");
ok(arm("none").judge === 3 && arm("chart").judge === 4, "judge scores unblinded to the right arms");

// manual /rate lines merge with the scan
const merged = mergeUses(
  [{ date: "2026-11-20", ts: "2026-11-20T11:00:00Z", skills: ["visualize"], first_try: true, source: "guess" }],
  [{ date: "2026-11-20", ts: "2026-11-20T12:00:00Z", skills: ["visualize"], first_try: false, source: "rated", note: "too long" },
   { date: "2026-11-21", ts: "2026-11-21T09:00:00Z", skills: ["design"], first_try: true, source: "rated", note: "" }]);
ok(merged.length === 2 && merged[0].first_try === false && merged[0].note === "too long", "a later /rate overrides the guess for the same use");

// verdicts
const mk = (s, ok_, n, d = "2026-11-2") => Array.from({ length: n }, (_, i) => ({ date: `${d}${i % 10}`, ts: `${d}${i % 10}T10:00:00Z`, skills: [s], first_try: i < ok_, fixes: i < ok_ ? 0 : 2, source: "guess", model: "test-model" }));
const a = analyze({ uses: [...mk("chart", 3, 10), ...mk("design", 9, 10)], history: [h], skills: ["chart", "design", "explore"], asOf: "2026-11-30" });
const v = (s) => a.rows.find((r) => r.name === s);
ok(v("chart").verdict === "Watch", `lab win that doesn't hold both ways -> Watch (got ${v("chart").verdict})`);
ok(v("design").verdict === "Keep", `right first try 90% over 10 uses -> Keep (got ${v("design").verdict})`);
ok(v("explore").verdict === "Watch", `no uses and no lab yet -> Watch (got ${v("explore").verdict})`);
const a2 = analyze({ uses: mk("chart", 3, 10), history: [], skills: ["chart"], asOf: "2026-11-30" });
ok(a2.rows[0].verdict === "Fix", "right first try 30% over 10 uses -> Fix");
ok(a2.needs.some((n) => n.verdict === "Re-test"), "a model with no lab run asks for a re-test");
ok(/Skill Health/.test(render(a)) && !/undefined|NaN/.test(render(a)), "page renders without undefined or NaN");

console.log(bad ? `\n${bad} failed` : "\nall passed");
process.exit(bad ? 1 : 0);
