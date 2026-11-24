// Print the exact prompt for one arm, so every run of a test uses the same words.
// node evals/combos/prompt.mjs <scenario> <arm> --skills <skills-dir> --out <dir>
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
const here = dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const opt = (k) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : undefined; };
const [sid, aid] = args;
const skills = resolve(opt("--skills") || resolve(here, "../../skills"));
const out = opt("--out");
if (!sid || !aid || !out) { console.error("usage: prompt.mjs <scenario> <arm> --skills <dir> --out <dir>"); process.exit(2); }
const { scenarios } = JSON.parse(readFileSync(resolve(here, "scenarios.json"), "utf8"));
const s = scenarios.find((x) => x.id === sid); const a = s?.arms.find((x) => x.id === aid);
if (!a) { console.error("unknown scenario or arm"); process.exit(2); }
const fixtures = resolve(here, s.fixtures);
const common = `The user is away and cannot answer: make the best choice yourself where you would ask, note it, and carry on. Do not spawn subagents. Setup: copy every file from ${fixtures} into DIR=${out} and work there. The main page goes at DIR/${s.output}. Node and Playwright with Chromium are installed.`;
const p = a.skills.length
  ? `You are a user's Claude Code session with these skills installed at ${skills}: ${a.skills.join(", ")}. When the user types /name, read ${skills}/<name>/SKILL.md and follow it, with the files it points to. Do not read other skills. Where a skill asks for a fresh reviewer agent, do a separate review pass yourself and say so. Do not edit anything under ${skills}. ${common}\n\nThe user typed:\n${s.task} ${a.invoke}\n\nEnd with the output path and the summary line of every checker you ran. Under 150 words.`
  : `Do the task below as you normally would. Do not read any files under ${skills} or ~/.claude/skills or ~/.agents/skills. ${common}\n\nThe user typed:\n${s.task}\n\nEnd with the output path and what you checked. Under 150 words.`;
console.log(p);
