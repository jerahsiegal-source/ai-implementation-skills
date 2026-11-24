// Read your local Claude Code and Codex session history and log each skill use:
// which skills ran, which model, how many follow-up asks came after, and any /rate you gave.
// Writes ~/.ai-skills/personal/usage-auto.jsonl (private, rebuilt each scan). Nothing leaves your computer.
//   node scan.mjs [--since 2026-10-01] [--claude-dir DIR] [--codex-dir DIR] [--out FILE] [--skills a,b,c]
import { existsSync, mkdirSync, readFileSync, readdirSync, realpathSync, statSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { basename, dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const home = homedir();
const claudeDir = resolve(opt("--claude-dir", join(process.env.CLAUDE_CONFIG_DIR || join(home, ".claude"), "projects")));
const codexDir = resolve(opt("--codex-dir", join(process.env.CODEX_HOME || join(home, ".codex"), "sessions")));
const out = resolve(opt("--out", join(home, ".ai-skills", "personal", "usage-auto.jsonl")));
const since = opt("--since", "");

// Which skills to look for: every folder in this repo's skills/ that is a real command.
const NOT_COMMANDS = new Set(["_template", "design-kit", "rate", "skill-review"]);
const repoSkills = (() => { try { return dirname(realpathSync(join(here, ".."))); } catch { return join(here, "..", ".."); } })();
const SKILLS = opt("--skills")
  ? opt("--skills").split(",")
  : readdirSync(repoSkills).filter((n) => !NOT_COMMANDS.has(n) && existsSync(join(repoSkills, n, "SKILL.md")));

// A follow-up that asks for a change. A guess, labeled as one; /rate always wins.
export const FIX = /\b(no|nope|not|wrong|instead|change|fix|again|redo|still|actually|didn'?t|doesn'?t|don'?t|isn'?t|aren'?t|too (?:long|short|big|small|much|busy|wordy|dark|light)|missing|broken|should|rather|undo|revert|why did)\b/i;

const files = (dir) => {
  if (!existsSync(dir)) return [];
  const res = [];
  const walk = (d, depth) => {
    for (const n of readdirSync(d)) {
      const p = join(d, n);
      const s = statSync(p);
      if (s.isDirectory()) { if (depth < 5 && n !== "subagents") walk(p, depth + 1); }
      else if (n.endsWith(".jsonl")) res.push(p);
    }
  };
  walk(dir, 0);
  return res;
};
const lines = (f) => readFileSync(f, "utf8").split("\n").filter(Boolean).map((l) => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
const textOf = (c) => typeof c === "string" ? c : Array.isArray(c) ? c.filter((x) => x && (x.type === "text" || x.type === "input_text")).map((x) => x.text).join("\n") : "";
const skillRe = new RegExp(`(?:^|[\\s(<>])[/$](${SKILLS.map((s) => s.replace(/[-]/g, "\\-")).join("|")})(?![\\w-])`, "g");
const rateRe = /(?:^|\s)[/$]rate(?:\s+(y|yes|n|no|\d)\b)?\s*(.*)$/is;

// Turn one user message into an event: a skill use, a rating, or a plain follow-up.
function classify(text) {
  const cmd = text.match(/<command-name>\s*[/$]?([\w:-]+)\s*<\/command-name>/);
  const cmdArgs = (text.match(/<command-args>([\s\S]*?)<\/command-args>/) || [])[1] || "";
  if (cmd) {
    const name = cmd[1].split(":").pop();
    if (name === "rate") return rateEvent(`/rate ${cmdArgs}`);
    const extra = [...cmdArgs.matchAll(skillRe)].map((m) => m[1]);
    if (SKILLS.includes(name)) return { kind: "use", skills: [...new Set([name, ...extra])] };
    if (extra.length) return { kind: "use", skills: [...new Set(extra)] };
    return null; // other built-in command
  }
  if (/^\s*<(system-reminder|local-command|wake|session-context|relay|task-notification)/.test(text) || /^Caveat:|^\[Request interrupted/.test(text)) return null;
  const r = rateEvent(text);
  if (r) return r;
  const used = [...text.matchAll(skillRe)].map((m) => m[1]);
  if (used.length) return { kind: "use", skills: [...new Set(used)], text };
  return { kind: "msg", text };
}
function rateEvent(text) {
  const m = text.match(rateRe);
  if (!m) return null;
  const v = (m[1] || "").toLowerCase();
  const first_try = v === "" ? null : /^(y|yes)$/.test(v) ? true : /^(n|no)$/.test(v) ? false : Number(v) >= 4;
  return { kind: "rate", first_try, note: (m[2] || "").trim().slice(0, 200) };
}

function claudeSession(f) {
  const ev = []; let model = null, cwd = null, session = basename(f, ".jsonl");
  for (const d of lines(f)) {
    if (d.isSidechain) continue;
    if (d.type === "assistant") {
      if (d.message?.model && !/synthetic/.test(d.message.model)) model = d.message.model;
      for (const c of Array.isArray(d.message?.content) ? d.message.content : [])
        if (c.type === "tool_use" && c.name === "Skill") {
          const s = String(c.input?.skill || "").split(":").pop();
          const last = ev[ev.length - 1];
          if (SKILLS.includes(s) && !(last?.kind === "use" && last.skills.includes(s))) ev.push({ kind: "use", skills: [s], t: d.timestamp, model, auto: true });
        }
      const last = ev[ev.length - 1]; if (last && !last.model) last.model = model;
      continue;
    }
    if (d.type !== "user" || d.isMeta) continue;
    const c = d.message?.content;
    if (Array.isArray(c) && c.some((x) => x.type === "tool_result")) continue;
    cwd = d.cwd || cwd;
    const e = classify(textOf(c));
    if (e) ev.push({ ...e, t: d.timestamp, model });
  }
  return { tool: "claude-code", session, cwd, ev };
}

function codexSession(f) {
  const ev = []; let model = null, cwd = null, session = basename(f, ".jsonl");
  for (const d of lines(f)) {
    const p = d.payload || {};
    if (d.type === "session_meta") { cwd = p.cwd || cwd; session = p.id || session; }
    if (d.type === "turn_context" && p.model) { model = p.model; const last = ev[ev.length - 1]; if (last && !last.model) last.model = model; }
    let text = null;
    if (d.type === "event_msg" && p.type === "user_message") text = p.message;
    if (text == null) continue;
    const e = classify(String(text));
    if (e) ev.push({ ...e, t: d.timestamp, model });
  }
  return { tool: "codex", session, cwd, ev };
}

// One row per skill use: follow-ups until the next use, and a /rate if one came before the next use.
export function toUses({ tool, session, cwd, ev }) {
  const rows = [];
  ev.forEach((e, i) => {
    if (e.kind !== "use") return;
    let j = i + 1, rate = null; const asks = [];
    for (; j < ev.length && ev[j].kind !== "use"; j++) {
      if (ev[j].kind === "rate" && !rate) rate = ev[j];
      if (ev[j].kind === "msg") asks.push(ev[j].text);
    }
    const fixAsks = asks.filter((a) => FIX.test(a));
    rows.push({
      date: (e.t || "").slice(0, 10), ts: e.t || null, tool, model: e.model || ev.slice(i).find((x) => x.model)?.model || null,
      skills: e.skills, project: cwd ? basename(cwd) : null, session,
      followups: asks.length, fixes: fixAsks.length,
      first_try: rate && rate.first_try !== null ? rate.first_try : fixAsks.length === 0,
      source: rate && rate.first_try !== null ? "rated" : "guess",
      note: rate?.note || "", asks: fixAsks.slice(0, 5).map((a) => a.replace(/\s+/g, " ").slice(0, 200)),
    });
  });
  return rows;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const sessions = [...files(claudeDir).map(claudeSession), ...files(codexDir).map(codexSession)];
  const rows = sessions.flatMap(toUses).filter((r) => !since || r.date >= since).sort((a, b) => String(a.ts).localeCompare(String(b.ts)));
  mkdirSync(dirname(out), { recursive: true });
  writeFileSync(out, rows.map((r) => JSON.stringify(r)).join("\n") + (rows.length ? "\n" : ""));
  const rated = rows.filter((r) => r.source === "rated").length;
  console.log(`${rows.length} skill uses found in ${sessions.length} sessions (${rated} rated by you) -> ${out}`);
}
