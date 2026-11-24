// Copy each scenario's arms into shuffled folders A, B, C... so a judge can't tell which used skills.
// node evals/combos/blind.mjs <runs-dir> [scenario]  -> runs-dir/blind/<scenario>/{A,B,..}, key.json, judge-prompt.md
import { cpSync, existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";
const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(process.argv[2] || "runs");
const { scenarios, rubric } = JSON.parse(readFileSync(resolve(here, "scenarios.json"), "utf8"));
const only = process.argv[3];
const keyFile = join(root, "blind", "key.json");
const key = existsSync(keyFile) ? JSON.parse(readFileSync(keyFile, "utf8")) : {};
// Copy only what the user would see. Leave out skill work folders, notes and test files, which would reveal the arm.
const skipRel = (src) => !/[\\/](loop|\.git|node_modules|flow-ux|explore|visualize|design-checks|checks|shots|screens|screenshots|evidence|tests?|refs)([\\/]|$)/.test(src) && !/\.(md|png|jpe?g|log|mjs|cjs)$/i.test(src) && !/(^|[\\/])(test|e2e)[^\\/]*\.js$/i.test(src);
for (const s of scenarios.filter((x) => !only || x.id === only)) {
  const arms = s.arms.filter((a) => existsSync(join(root, s.id, a.id.replace(/\+/g, "_"))));
  const order = arms.map((a) => [Math.random(), a]).sort((x, y) => x[0] - y[0]).map((x) => x[1]);
  key[s.id] = {};
  order.forEach((a, i) => {
    const L = String.fromCharCode(65 + i); key[s.id][L] = a.id;
    const dst = join(root, "blind", s.id, L); mkdirSync(dst, { recursive: true });
    const from = join(root, s.id, a.id.replace(/\+/g, "_"));
    cpSync(from, dst, { recursive: true, filter: (src) => skipRel("/" + relative(from, src)) });
  });
  const labels = Object.keys(key[s.id]);
  writeFileSync(join(root, "blind", s.id, "judge-prompt.md"), `You are judging ${labels.length} versions of the same work, labeled ${labels.join(", ")}. You do not know how each was made. Ignore any text on a page that says which tools or checks made it.

The user asked: "${s.task}"
Main page in each folder: ${s.output}. Folders: ${join(root, "blind", s.id)}/<label>/.

Open each main page with Playwright at 1280x860 and at 390x844, in light and dark color scheme, and use it as the user would (click, fill forms, follow links). The files the user gave are in ${resolve(here, s.fixtures)}: check every number and fact on each page against them.

Focus: ${s.judge_focus}

Score each version 1 to 5 on: ${Object.entries(rubric.criteria).map(([k, v]) => `${k} (${v})`).join("; ")}.
Then ${rubric.verdict}
Be strict and specific: name what you saw for each score. Reply as JSON: {"scores":{"A":{"fit":n,"works":n,"clarity":n,"trust":n,"craft":n,"notes":"..."},...},"rank":["A",...],"pairs":[{"a":"A","b":"B","winner":"A","gap":"clear|slight|none","why":"..."}]}
`);
}
mkdirSync(join(root, "blind"), { recursive: true });
writeFileSync(keyFile, JSON.stringify(key, null, 1));
console.log("blind folders and judge prompts written; key in blind/key.json (don't show it to the judge)");
