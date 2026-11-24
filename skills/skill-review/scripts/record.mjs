// Turn a finished combo-kit lab run (evals/combos) into one history file, so results can be compared across models.
//   node record.mjs <runs-dir> --model claude-opus-5-5 --tool claude-code [--blind2 <runs-dir>/blind-2] [--date 2026-11-24] [--note "..."] [--out evals/history]
// Reads: runs/scores.json, runs/costs.json, runs/blind/key.json + runs/blind/<scenario>/verdict.json (and the same in --blind2 if given).
import { existsSync, mkdirSync, readFileSync, realpathSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const root = resolve(args[0] && !args[0].startsWith("--") ? args[0] : "runs");
const model = opt("--model"); const tool = opt("--tool", "claude-code");
if (!model) { console.error("usage: record.mjs <runs-dir> --model <id> [--tool claude-code|codex] [--blind2 dir] [--note text]"); process.exit(2); }
const date = opt("--date", new Date().toISOString().slice(0, 10));
const repo = (() => { try { return resolve(realpathSync(here), "../../.."); } catch { return resolve(here, "../../.."); } })();
const outDir = resolve(opt("--out", join(repo, "evals", "history")));
const read = (f) => (existsSync(f) ? JSON.parse(readFileSync(f, "utf8")) : null);

const scores = read(join(root, "scores.json")) || {};
const costs = read(join(root, "costs.json")) || {};
const CRIT = ["fit", "works", "clarity", "trust", "craft"];

// Unblind one judge pass: { scenario: { armId: {judge, rank}, pairs: [{a,b,winner,gap}] } }
function judgePass(dir) {
  const key = read(join(dir, "key.json")); if (!key) return null;
  const res = {};
  for (const [sid, map] of Object.entries(key)) {
    const v = read(join(dir, sid, "verdict.json")); if (!v) continue;
    const arm = (L) => map[L] || L;
    const arms = {};
    for (const [L, s] of Object.entries(v.scores || {})) {
      const nums = CRIT.map((c) => Number(s[c])).filter((n) => !Number.isNaN(n));
      arms[arm(L)] = { judge: nums.length ? +(nums.reduce((a, b) => a + b, 0) / nums.length).toFixed(2) : null, notes: s.notes || "" };
    }
    (v.rank || []).forEach((L, i) => { if (arms[arm(L)]) arms[arm(L)].rank = i + 1; });
    res[sid] = { arms, pairs: (v.pairs || []).map((p) => ({ a: arm(p.a), b: arm(p.b), winner: p.winner ? arm(p.winner) : null, gap: p.gap || "none" })) };
  }
  return res;
}
// Result of arm vs baseline in one pass: win / loss / tie, from the judge's pair call (or its scores if no pair).
function vs(pass, sid, armId, base = "none") {
  const s = pass?.[sid]; if (!s) return null;
  const p = s.pairs.find((x) => (x.a === armId && x.b === base) || (x.a === base && x.b === armId));
  if (p) return p.gap === "none" || !p.winner ? { r: "tie", gap: "none" } : { r: p.winner === armId ? "win" : "loss", gap: p.gap };
  const a = s.arms[armId]?.judge, b = s.arms[base]?.judge;
  if (a == null || b == null) return null;
  const d = a - b; return Math.abs(d) < 0.3 ? { r: "tie", gap: "none" } : { r: d > 0 ? "win" : "loss", gap: Math.abs(d) >= 1 ? "clear" : "slight" };
}

const p1 = judgePass(join(root, "blind"));
const p2 = opt("--blind2") ? judgePass(resolve(opt("--blind2"))) : null;
const sids = [...new Set([...Object.keys(scores), ...Object.keys(p1 || {}), ...Object.keys(costs).map((k) => k.split("/")[0])])];
const scenarios = sids.map((sid) => {
  const armIds = [...new Set([...Object.keys(scores[sid] || {}), ...Object.keys(p1?.[sid]?.arms || {}), ...Object.keys(costs).filter((k) => k.startsWith(sid + "/")).map((k) => k.slice(sid.length + 1))])];
  const arms = armIds.map((id) => {
    const sc = scores[sid]?.[id] || {}; const c = costs[`${sid}/${id}`] || {};
    const j1 = p1?.[sid]?.arms[id]; const j2 = p2?.[sid]?.arms[id];
    let vsNone = null;
    if (id !== "none") {
      const a = vs(p1, sid, id), b = p2 ? vs(p2, sid, id) : null;
      if (a) vsNone = { result: a.r, gap: a.gap, holds: b ? b.r === a.r : null, second: b ? b.r : null };
    }
    return {
      arm: id, skills: id === "none" ? [] : id.split("+"),
      pages: sc.pages ?? null, fail: sc.fail ?? null, warn: sc.warn ?? null,
      tokens: c.tokens ?? null, seconds: c.seconds ?? null,
      judge: j1?.judge ?? null, judge2: j2?.judge ?? null, rank: j1?.rank ?? null,
      vsNone, judgeNotes: (j1?.notes || "").slice(0, 300),
    };
  });
  return { id: sid, arms };
});

const entry = { date, model, tool, note: opt("--note", ""), bothOrders: !!p2, scenarios };
mkdirSync(outDir, { recursive: true });
const file = join(outDir, `${date}-${model.replace(/[^\w.-]+/g, "_")}-${tool}.json`);
writeFileSync(file, JSON.stringify(entry, null, 1) + "\n");
console.log(`recorded ${scenarios.length} tasks, ${scenarios.reduce((n, s) => n + s.arms.length, 0)} arms -> ${file}`);
