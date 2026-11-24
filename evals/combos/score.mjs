// Run both checkers on every arm's output and write scores.json.
// node evals/combos/score.mjs <runs-dir>   (runs-dir/<scenario>/<arm>/<output>)
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(process.argv[2] || "runs");
const kit = resolve(here, "../../skills/design-kit/scripts/check-page.mjs");
const chart = resolve(here, "../../skills/chart/scripts/check-chart.mjs");
const run = (f, args) => { try { return JSON.parse(execFileSync("node", [f, ...args], { encoding: "utf8", maxBuffer: 1 << 26 })); } catch (e) { try { return JSON.parse(e.stdout); } catch { return null; } } };
const { scenarios } = JSON.parse(readFileSync(resolve(here, "scenarios.json"), "utf8"));
const out = {};
for (const s of scenarios) for (const a of s.arms) {
  const dir = join(root, s.id, a.id.replace(/\+/g, "_"));
  if (!existsSync(dir)) continue;
  const pages = readdirSync(dir, { recursive: true }).filter((f) => String(f).endsWith(".html") && !/node_modules|shots|\/loop\//.test(String(f)));
  const rows = pages.map((f) => {
    const p = join(dir, String(f));
    const pg = run(kit, [p, "--json"]); const ch = run(chart, [p, "--json"]);
    const ids = (r) => (r?.results || []).filter((x) => x.status === "fail" || x.status === "warn").map((x) => `${x.status}:${x.id}`);
    return { page: String(f), fail: (pg?.summary?.failed ?? 0) + (ch?.failed ?? 0), warn: (pg?.summary?.warned ?? 0) + (ch?.warned ?? 0), charts: ch?.checked ?? 0, issues: [...ids(pg), ...ids(ch)] };
  });
  (out[s.id] ||= {})[a.id] = { pages: rows.length, fail: rows.reduce((n, r) => n + r.fail, 0), warn: rows.reduce((n, r) => n + r.warn, 0), rows };
  console.log(`${s.id} / ${a.id}: ${rows.length} pages, ${out[s.id][a.id].fail} FAIL, ${out[s.id][a.id].warn} WARN`);
}
writeFileSync(join(root, "scores.json"), JSON.stringify(out, null, 1));
