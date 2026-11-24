// Add one rating line to your private usage log. Never writes inside the repo.
//   node rate.mjs --first-try y|n --skills design,chart [--fixes 2] [--note "too long"] [--model X] [--tool claude-code|codex|claude-app]
import { appendFileSync, mkdirSync } from "node:fs";
import { homedir } from "node:os";
import { basename, dirname, join, resolve } from "node:path";

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 && args[i + 1] !== undefined ? args[i + 1] : d; };
const ft = String(opt("--first-try", "")).toLowerCase();
if (!/^(y|yes|n|no)$/.test(ft)) { console.error("usage: rate.mjs --first-try y|n --skills a,b [--fixes N] [--note text] [--model X] [--tool T]"); process.exit(2); }
const out = resolve(opt("--out", join(homedir(), ".ai-skills", "personal", "usage-log.jsonl")));
const now = new Date();
const row = {
  date: now.toISOString().slice(0, 10), ts: now.toISOString(),
  tool: opt("--tool", "unknown"), model: opt("--model", null),
  skills: String(opt("--skills", "")).split(",").map((s) => s.trim().replace(/^[/$]/, "")).filter(Boolean),
  project: basename(process.cwd()),
  first_try: /^y/.test(ft), fixes: opt("--fixes") !== undefined ? Number(opt("--fixes")) : null,
  source: "rated", note: String(opt("--note", "")).slice(0, 200),
};
mkdirSync(dirname(out), { recursive: true });
appendFileSync(out, JSON.stringify(row) + "\n");
console.log(`Logged: ${row.skills.join("+") || "no skill"} · ${row.first_try ? "right first try" : "needed fixes"}${row.note ? ` · ${row.note}` : ""}`);
