// Build the Skill Health page from real use (private logs) and lab history (evals/history in the repo).
//   node dashboard.mjs [--personal ~/.ai-skills/personal] [--history <repo>/evals/history] [--out <personal>/skill-health.html] [--as-of 2026-11-24] [--demo]
// Also writes skill-health.json beside the page, which /skill-review reads.
import { existsSync, mkdirSync, readFileSync, readdirSync, realpathSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const real = (p) => { try { return realpathSync(p); } catch { return p; } };
const repo = resolve(real(here), "../../..");
const RULES = JSON.parse(readFileSync(join(here, "..", "rules.json"), "utf8"));
const DAY = 864e5;

const readJsonl = (f) => (existsSync(f) ? readFileSync(f, "utf8").split("\n").filter(Boolean).map((l) => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean) : []);

// Your /rate lines win over the scanner's guess for the same use; a /rate the scanner already saw isn't counted twice.
export function mergeUses(auto, manual) {
  const rated = auto.filter((r) => r.source === "rated").map((r) => Date.parse(r.ts));
  const extra = manual.filter((m) => {
    const t = Date.parse(m.ts);
    if (rated.some((x) => Math.abs(x - t) < 15 * 6e4)) return false; // same rating, seen in the transcript
    // A manual rating overrides the latest guessed use of the same skills in the 6 hours before it.
    const target = auto.filter((r) => r.source === "guess" && Date.parse(r.ts) <= t && t - Date.parse(r.ts) < 6 * 36e5 && r.skills.join() === m.skills.join()).pop();
    if (target) { Object.assign(target, { first_try: m.first_try, source: "rated", note: m.note, fixes: m.fixes ?? target.fixes }); return false; }
    return true;
  });
  return [...auto, ...extra].sort((a, b) => String(a.ts).localeCompare(String(b.ts)));
}

export function loadHistory(dir) {
  if (!existsSync(dir)) return [];
  return readdirSync(dir).filter((f) => f.endsWith(".json")).map((f) => ({ file: f, ...JSON.parse(readFileSync(join(dir, f), "utf8")) })).sort((a, b) => a.date.localeCompare(b.date));
}

// What the lab says about one arm (a single skill, or a stack like "chart+visualize") in one history entry.
function labFor(entry, armId) {
  const res = [];
  for (const s of entry.scenarios || []) {
    const a = s.arms.find((x) => x.arm === armId); if (!a) continue;
    const none = s.arms.find((x) => x.arm === "none");
    res.push({ task: s.id, result: a.vsNone?.result || null, gap: a.vsNone?.gap || null, holds: a.vsNone?.holds ?? null,
      fail: a.fail, cost: none?.tokens && a.tokens ? +(a.tokens / none.tokens).toFixed(1) : null, judge: a.judge, judgeNone: none?.judge ?? null });
  }
  return res.length ? { model: entry.model, tool: entry.tool, date: entry.date, both: !!entry.bothOrders, res } : null;
}
const wins = (l) => l.res.some((r) => r.result === "win" && r.holds !== false);
const clearWin = (l) => l.res.some((r) => r.result === "win" && r.gap === "clear" && r.holds !== false);

export function analyze({ uses, history, skills, asOf = new Date().toISOString().slice(0, 10), rules = RULES }) {
  const now = Date.parse(asOf);
  const earliest = uses.length ? Date.parse(uses[0].ts || uses[0].date) : now;
  const names = [...new Set([...skills, ...uses.flatMap((u) => u.skills)])].filter((n) => n !== "none");
  const rows = names.map((name) => {
    const mine = uses.filter((u) => u.skills.includes(name));
    const win = mine.slice(-rules.window);
    const rate = win.length ? win.filter((u) => u.first_try).length / win.length : null;
    const lastUsed = mine.length ? mine[mine.length - 1].date : null;
    const labs = history.map((h) => labFor(h, name)).filter(Boolean);
    const lab = labs[labs.length - 1] || null, prev = labs[labs.length - 2] || null;
    const cost = lab ? lab.res.map((r) => r.cost).filter(Boolean) : [];
    const costRatio = cost.length ? +(cost.reduce((a, b) => a + b, 0) / cost.length).toFixed(1) : null;
    let verdict = "Keep", why = "Beats plain Claude and gets it right first try";
    if (lab && !wins(lab) && prev && !wins(prev)) { verdict = "Cut"; why = `Tied plain Claude on ${prev.model} and ${lab.model}`; }
    else if (lab && !wins(lab)) { verdict = "Watch"; why = `No blind win on ${lab.model}. Re-test once before cutting`; }
    else if (win.length >= rules.min_uses && rate < rules.first_try_target) { verdict = "Fix"; why = `Right first try ${Math.round(rate * 100)}% of last ${win.length} uses`; }
    else if (now - earliest >= rules.unused_days * DAY && (!lastUsed || now - Date.parse(lastUsed) > rules.unused_days * DAY)) { verdict = "Cut"; why = `Not used in ${rules.unused_days} days`; }
    else if (lab && costRatio && costRatio > rules.cost_ratio_trim && !clearWin(lab)) { verdict = "Trim"; why = `${costRatio}x the tokens of plain Claude without a clear win`; }
    else if (win.length < rules.min_uses && !lab) { verdict = "Watch"; why = "Not enough data yet"; }
    else if (win.length < rules.min_uses) { why = "Wins in the lab. Few real uses yet"; }
    const misses = mine.filter((u) => !u.first_try).slice(-8).reverse().map((u) => ({ date: u.date, note: u.note || "", asks: u.asks || [], source: u.source, project: u.project || "" }));
    return {
      name, verdict, why, uses: mine.length, recent: mine.filter((u) => now - Date.parse(u.date) <= rules.recent_days * DAY).length,
      rate, n: win.length, rated: win.filter((u) => u.source === "rated").length,
      fixes: win.length ? +(win.reduce((a, u) => a + (u.fixes || 0), 0) / win.length).toFixed(1) : null,
      lastUsed, lab, labs, costRatio, misses,
    };
  });
  // Stacks from the lab: does the stack beat plain Claude, and its best single skill?
  const last = history[history.length - 1];
  const stacks = [];
  for (const s of last?.scenarios || []) for (const a of s.arms) if (a.skills?.length > 1) {
    const singles = s.arms.filter((x) => x.skills?.length === 1 && a.skills.includes(x.skills[0]) && x.judge != null);
    const best = singles.sort((x, y) => y.judge - x.judge)[0];
    const none = s.arms.find((x) => x.arm === "none");
    stacks.push({ task: s.id, arm: a.arm, vsNone: a.vsNone, judge: a.judge, best: best ? { arm: best.arm, judge: best.judge } : null,
      cost: none?.tokens && a.tokens ? +(a.tokens / none.tokens).toFixed(1) : null, fail: a.fail,
      addsValue: best ? a.judge - best.judge >= 0.3 : null });
  }
  // Monthly trend of the north star.
  const months = {};
  for (const u of uses) { const m = u.date.slice(0, 7); (months[m] ||= { m, n: 0, ok: 0 }); months[m].n++; if (u.first_try) months[m].ok++; }
  const trend = Object.values(months).sort((a, b) => a.m.localeCompare(b.m)).slice(-6).map((x) => ({ ...x, rate: x.ok / x.n }));
  const recentUses = uses.filter((u) => now - Date.parse(u.date) <= rules.recent_days * DAY);
  const latestModel = [...uses].reverse().find((u) => u.model)?.model || null;
  const labModels = new Set(history.map((h) => h.model));
  const needs = [];
  for (const r of rows) if (["Fix", "Cut", "Trim"].includes(r.verdict)) needs.push({ skill: r.name, verdict: r.verdict, why: r.why });
  if (latestModel && !labModels.has(latestModel)) needs.unshift({ skill: "lab", verdict: "Re-test", why: `You're using ${latestModel}, which has no lab run yet` });
  if (last && now - Date.parse(last.date) > 90 * DAY) needs.push({ skill: "lab", verdict: "Re-test", why: `Last lab run was ${last.date}` });
  for (const s of stacks) if (s.addsValue === false) needs.push({ skill: s.arm, verdict: "Trim", why: `Stack no better than ${s.best.arm} on ${s.task}` });
  return {
    asOf, rules, rows, stacks, trend, needs, latestModel,
    total: { uses: recentUses.length, rate: recentUses.length ? recentUses.filter((u) => u.first_try).length / recentUses.length : null,
      fixes: recentUses.length ? +(recentUses.reduce((a, u) => a + (u.fixes || 0), 0) / recentUses.length).toFixed(1) : null,
      rated: recentUses.filter((u) => u.source === "rated").length },
    lastLab: last ? { date: last.date, model: last.model, tool: last.tool, both: !!last.bothOrders } : null,
    models: [...labModels],
  };
}

// Sample data for a preview, clearly labeled on the page. Deterministic.
function demo(asOf) {
  let seed = 7; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
  const plan = { design: 0.72, visualize: 0.8, explore: 0.6, chart: 0.38, "flow-ux": 0.66, "work-loop": 0.7, "intent-brief": 0.85 };
  const notes = { chart: ["wrong chart type", "labels overlap on phone", "too many colors"], explore: ["concepts too similar"], design: ["too much text"] };
  const uses = []; const end = Date.parse(asOf);
  for (let d = 150; d >= 0; d--) for (const [s, p] of Object.entries(plan)) {
    if (s === "intent-brief" && d < 70) continue;
    if (rnd() > (s === "design" || s === "visualize" ? 0.35 : 0.14)) continue;
    const ok = rnd() < p + (150 - d) / 1500; const t = new Date(end - d * DAY).toISOString();
    uses.push({ date: t.slice(0, 10), ts: t, tool: rnd() < 0.75 ? "claude-code" : "codex", model: d > 40 ? "claude-opus-5" : "claude-opus-5-5",
      skills: rnd() < 0.15 && s === "visualize" ? ["chart", "visualize"] : [s], fixes: ok ? 0 : 1 + Math.floor(rnd() * 3), first_try: ok,
      source: rnd() < 0.4 ? "rated" : "guess", note: ok ? "" : (notes[s] || ["needed changes"])[Math.floor(rnd() * (notes[s]?.length || 1))], asks: ok ? [] : ["make it shorter and fix the labels"], project: "sample" });
  }
  const arm = (arm, judge, tokens, fail, r, gap, holds) => ({ arm, skills: arm === "none" ? [] : arm.split("+"), fail, warn: 1, tokens, seconds: tokens / 900, judge, vsNone: arm === "none" ? null : { result: r, gap, holds } });
  const mk = (date, model, x) => ({ date, model, tool: "claude-code", bothOrders: true, scenarios: [
    { id: "cafe-report", arms: [arm("none", 2.8, 40000, 2), arm("chart", 3.4 + x, 52000, 0, "win", "slight", true), arm("visualize", 4.1 + x, 61000, 0, "win", "clear", true), arm("chart+visualize+design", 4.2, 98000, 0, "win", "clear", true)] },
    { id: "signup-build", arms: [arm("none", 3.0, 45000, 1), arm("design", 3.9, 58000, 0, "win", "clear", true), arm("design+flow-ux", 4.4, 90000, 0, "win", "clear", true)] },
    { id: "client-tracker", arms: [arm("none", 3.1, 50000, 1), arm("design", 3.8, 66000, 0, "win", "slight", true), arm("intent-brief+explore+design+work-loop", 4.5, 210000, 0, "win", "clear", true)] },
    { id: "explore-dir", arms: [arm("none", 3.3, 60000, 2), arm("explore", 3.4, 140000, 0, x > 0 ? "tie" : "win", x > 0 ? "none" : "slight", true)] },
  ] });
  return { uses, history: [mk("2026-08-02", "claude-opus-5", 0), mk("2026-11-24", "claude-opus-5-5", 0.1)] };
}

// ---------- page ----------
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const pct = (x) => (x == null ? "–" : `${Math.round(x * 100)}%`);
const CLS = { Keep: "ok", Fix: "warn", Trim: "warn", Cut: "bad", Watch: "mute", "Re-test": "acc" };
const fmtDate = (d) => (d ? new Date(d + "T12:00:00Z").toLocaleDateString("en-US", { day: "numeric", month: "short", year: "numeric" }) : "–");

export function render(a, { sample = false } = {}) {
  const attention = a.rows.filter((r) => ["Fix", "Cut", "Trim"].includes(r.verdict)).length;
  const health = attention === 0 ? ["ok", "Healthy"] : attention <= 2 ? ["warn", "Needs a look"] : ["bad", "Needs work"];
  const keep = a.rows.filter((r) => r.verdict === "Keep").length;
  const verdict = a.total.rate == null
    ? "No real-use data yet. Use the skills, then run /skill-review again."
    : `Right first try ${pct(a.total.rate)} of the time in the last ${a.rules.recent_days} days. ${keep} of ${a.rows.length} skills on track.`;
  const bar = (r, n) => `<span class="meter" aria-hidden="true"><i style="width:${Math.round((r || 0) * 100)}%"></i><b style="left:${a.rules.first_try_target * 100}%"></b></span>`;
  const labCell = (r) => {
    if (!r.lab) return `<span class="mute">Not tested</span>`;
    const w = r.lab.res.filter((x) => x.result === "win" && x.holds !== false).length;
    return `<b>${w} of ${r.lab.res.length}</b> <span class="mute">tasks won</span>`;
  };
  const row = (r) => `<details class="sk">
   <summary>
    <span class="nm">/${esc(r.name)}</span>
    <span class="chip ${CLS[r.verdict]}">${r.verdict}</span>
    <span class="ft">${bar(r.rate)}<b class="num">${pct(r.rate)}</b><span class="mute">${r.n ? `of ${r.n}` : ""}</span></span>
    <span class="num">${r.fixes ?? "–"}</span>
    <span class="num">${r.recent}</span>
    <span>${labCell(r)}</span>
    <span class="num">${r.costRatio ? r.costRatio + "x" : "–"}</span>
   </summary>
   <div class="more">
    <p class="why">${esc(r.why)}</p>
    <div class="cols">
     <div><h4>Recent misses</h4>${r.misses.length ? `<ul>${r.misses.map((m) => `<li><span class="mute">${fmtDate(m.date)}${m.source === "guess" ? " · guessed" : ""}</span> ${esc(m.note || m.asks[0] || "needed changes")}</li>`).join("")}</ul>` : `<p class="mute">None</p>`}</div>
     <div><h4>Lab by model</h4>${r.labs.length ? `<ul>${r.labs.map((l) => `<li><b>${esc(l.model)}</b> <span class="mute">${fmtDate(l.date)}</span><br>${l.res.map((x) => `${esc(x.task)}: <span class="chip sm ${x.result === "win" ? "ok" : x.result === "loss" ? "bad" : "mute"}">${x.result || "–"}${x.gap && x.result === "win" ? ", " + x.gap : ""}</span>${x.holds === false ? ` <span class="mute">flips when swapped</span>` : ""}`).join("<br>")}</li>`).join("")}</ul>` : `<p class="mute">No lab run yet</p>`}</div>
    </div>
   </div>
  </details>`;
  const stackRows = a.stacks.map((s) => `<tr><td><b>${esc(s.arm.split("+").map((x) => "/" + x).join(" + "))}</b><br><span class="mute">${esc(s.task)}</span></td>
   <td><span class="chip ${s.vsNone?.result === "win" ? "ok" : "mute"}">${s.vsNone?.result || "–"}${s.vsNone?.gap && s.vsNone.result === "win" ? ", " + s.vsNone.gap : ""}</span></td>
   <td>${s.best ? `<span class="chip ${s.addsValue ? "ok" : "warn"}">${s.addsValue ? "better" : "no better"}</span> <span class="mute">than /${esc(s.best.arm)}</span>` : "–"}</td>
   <td class="num">${s.cost ? s.cost + "x" : "–"}</td></tr>`).join("");
  const trendBars = a.trend.length ? a.trend.map((t) => `<div class="tb" title="${t.n} uses"><span class="tv num">${pct(t.rate)}</span><span class="col" style="height:${Math.max(6, Math.round(t.rate * 90))}px"></span><span class="tl">${new Date(t.m + "-15").toLocaleDateString("en-US", { month: "short" })}</span></div>`).join("") : `<p class="mute">No data yet</p>`;
  return `<!doctype html><html lang="en" data-look="studio"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Skill Health</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&display=swap">
<style>
:root{--bg:#FFFFFF;--surface:#FFFFFF;--sunk:#F1F3F6;--ink:#0F141C;--muted:#535D6C;--line:#D9DEE5;--accent:#2F3FD0;--accent-soft:#ECEEFC;--ok:#17704A;--ok-soft:#E3F3EA;--warn:#9A5B00;--warn-soft:#FDF0DC;--bad:#A82E25;--bad-soft:#FBE2DF;--r:6px;--f:"IBM Plex Sans",system-ui,"Segoe UI",sans-serif;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#11161D;--surface:#18202A;--sunk:#222C38;--ink:#E8EDF2;--muted:#A5B0BD;--line:#2F3A47;--accent:#8E9BFF;--accent-soft:#1F2547;--ok:#5FCB8F;--ok-soft:#163324;--warn:#F2C36B;--warn-soft:#30291B;--bad:#EF8A82;--bad-soft:#3C2220;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#11161D;--surface:#18202A;--sunk:#222C38;--ink:#E8EDF2;--muted:#A5B0BD;--line:#2F3A47;--accent:#8E9BFF;--accent-soft:#1F2547;--ok:#5FCB8F;--ok-soft:#163324;--warn:#F2C36B;--warn-soft:#30291B;--bad:#EF8A82;--bad-soft:#3C2220;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.55 var(--f)}
.wrap{max-width:1120px;margin:0 auto;padding:32px max(16px,env(safe-area-inset-right,0px)) 80px max(16px,env(safe-area-inset-left,0px));display:flex;flex-direction:column;gap:26px}
h1,h2,h3,h4{margin:0;font-weight:600;line-height:1.15;letter-spacing:-.02em;text-wrap:balance}
h1{font-size:clamp(28px,4vw,38px)}h2{font-size:22px}h4{font-size:15px;margin-bottom:6px}
p{margin:0}.mute{color:var(--muted)}.num{font-variant-numeric:tabular-nums;font-weight:600}
.say{font-size:20px;line-height:1.45;color:var(--muted);max-width:62ch}
.pill{display:inline-flex;font-weight:700;font-size:15px;padding:4px 12px;border-radius:99px}
.chip{display:inline-block;justify-self:start;font-size:13px;font-weight:700;padding:2px 10px;border-radius:99px;white-space:nowrap}
.chip.sm{font-size:12px;padding:0 8px}
.ok{background:var(--ok-soft);color:var(--ok)}.warn{background:var(--warn-soft);color:var(--warn)}.bad{background:var(--bad-soft);color:var(--bad)}.mute.chip{background:var(--sunk)}.acc{background:var(--accent-soft);color:var(--accent)}
.sample{background:var(--accent-soft);color:var(--accent);border-radius:var(--r);padding:10px 14px;font-weight:600;font-size:15px}
.need{background:var(--warn-soft);border-radius:var(--r);padding:16px 18px;display:flex;flex-direction:column;gap:8px}
.need>b{color:var(--warn)}.need ul{margin:0;padding-left:0;list-style:none;display:flex;flex-direction:column;gap:6px}.need li{display:flex;flex-wrap:wrap;gap:2px 10px;align-items:baseline}.need li .chip{min-width:56px;text-align:center}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.tile{border:1px solid var(--line);border-radius:var(--r);padding:14px 16px;display:flex;flex-direction:column;gap:4px;min-width:0}
.tile.star{border:2px solid var(--accent)}.tile .k{font-size:13px;font-weight:700;color:var(--muted)}.tile .big{font-size:34px;font-weight:600;font-variant-numeric:tabular-nums;line-height:1.1}
.trend{display:flex;align-items:flex-end;gap:10px;height:130px;padding-top:8px}
.tb{display:flex;flex-direction:column;align-items:center;gap:4px;flex:1;min-width:0}.tb .col{width:100%;max-width:44px;background:var(--accent);border-radius:3px 3px 0 0}.tv{font-size:13px}.tl{font-size:13px;color:var(--muted)}
.head,.sk summary{display:grid;grid-template-columns:1.3fr .8fr 1.8fr .7fr .6fr 1.3fr .6fr;gap:10px;align-items:center;padding:10px 12px}
.head{font-size:13px;font-weight:700;color:var(--muted);border-bottom:1px solid var(--line)}
.sk{border-bottom:1px solid var(--line)}.sk summary{cursor:pointer;list-style:none}.sk summary::-webkit-details-marker{display:none}
.sk summary:hover{background:var(--sunk)}.sk summary:focus-visible{outline:3px solid var(--accent);outline-offset:-3px}
.nm{font-weight:700}.ft{display:flex;align-items:center;gap:8px}
.meter{position:relative;flex:1;max-width:120px;height:8px;background:var(--sunk);border-radius:99px}.meter i{position:absolute;inset:0 auto 0 0;background:var(--accent);border-radius:99px}.meter b{position:absolute;top:-3px;bottom:-3px;width:2px;background:var(--ink);opacity:.5}
.more{padding:4px 12px 16px;display:flex;flex-direction:column;gap:12px}.why{font-weight:600}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:20px}.cols ul{margin:0;padding-left:18px;display:flex;flex-direction:column;gap:6px;font-size:15px}
.tw{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:15px;min-width:560px}th,td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}th{font-size:13px;color:var(--muted)}
@media (max-width:760px){.head{display:none}.sk summary{grid-template-columns:1fr auto;row-gap:4px}.sk summary>span:nth-child(n+3){grid-column:1/-1;font-size:15px}.sk summary>span:nth-child(4)::before{content:"Fix rounds ";color:var(--muted);font-weight:400}.sk summary>span:nth-child(5)::before{content:"Uses, ${a.rules.recent_days} days ";color:var(--muted);font-weight:400}.sk summary>span:nth-child(7)::before{content:"Cost vs plain ";color:var(--muted);font-weight:400}.cols{grid-template-columns:1fr}}
</style></head><body><main class="wrap">
${sample ? `<p class="sample">Sample data. Run /skill-review to see your own.</p>` : ""}
<header style="display:flex;flex-direction:column;gap:10px">
 <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap"><span class="pill ${health[0]}">${health[1]}</span><span class="mute" style="font-size:14px">${fmtDate(a.asOf)}</span></div>
 <h1>Skill Health</h1>
 <p class="say">${esc(verdict)}</p>
</header>
${a.needs.length ? `<section class="need"><b>Needs you · ${a.needs.length}</b><ul>${a.needs.map((n) => `<li><span class="chip ${CLS[n.verdict] || "warn"}">${n.verdict}</span> <b>${n.skill === "lab" ? "Lab" : "/" + esc(n.skill.split("+").join(" + /"))}</b> <span class="mute">${esc(n.why)}</span></li>`).join("")}</ul></section>` : ""}
<section class="tiles">
 <div class="tile star"><span class="k">Right first try · ${a.rules.recent_days} days</span><span class="big">${pct(a.total.rate)}</span><span class="mute">${a.total.uses} uses · ${a.total.rated} rated by you</span></div>
 <div class="tile"><span class="k">Fix rounds per use</span><span class="big">${a.total.fixes ?? "–"}</span><span class="mute">Lower is better</span></div>
 <div class="tile"><span class="k">Last lab run</span><span class="big" style="font-size:22px">${a.lastLab ? esc(a.lastLab.model) : "None yet"}</span><span class="mute">${a.lastLab ? `${fmtDate(a.lastLab.date)} · ${a.lastLab.both ? "judged both orders" : "one judge pass"}` : "Run the combo tests"}</span></div>
 <div class="tile"><span class="k">Right first try by month</span><div class="trend">${trendBars}</div></div>
</section>
<section style="display:flex;flex-direction:column;gap:8px">
 <h2>Skills</h2>
 <div class="head"><span>Skill</span><span>Verdict</span><span>Right first try, last ${a.rules.window}</span><span>Fix rounds</span><span>Uses</span><span>Lab vs plain Claude</span><span>Cost</span></div>
 ${a.rows.map(row).join("")}
 <p class="mute" style="font-size:14px">Line on each bar: the ${pct(a.rules.first_try_target)} goal. Click a skill for its misses and lab history.</p>
</section>
${a.stacks.length ? `<section style="display:flex;flex-direction:column;gap:8px"><h2>Stacks</h2><div class="tw"><table><thead><tr><th>Stack</th><th>vs plain Claude</th><th>vs best single skill</th><th>Cost</th></tr></thead><tbody>${stackRows}</tbody></table></div></section>` : ""}
</main></body></html>`;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
  const personal = resolve(opt("--personal", join(homedir(), ".ai-skills", "personal")));
  const asOf = opt("--as-of", new Date().toISOString().slice(0, 10));
  const isDemo = args.includes("--demo");
  const skillsDir = resolve(repo, "skills");
  const skills = existsSync(skillsDir) ? readdirSync(skillsDir).filter((n) => !["_template", "design-kit", "rate", "skill-review"].includes(n) && existsSync(join(skillsDir, n, "SKILL.md"))) : [];
  let uses, history;
  if (isDemo) ({ uses, history } = demo(asOf));
  else {
    uses = mergeUses(readJsonl(join(personal, "usage-auto.jsonl")), readJsonl(join(personal, "usage-log.jsonl")));
    history = loadHistory(resolve(opt("--history", join(repo, "evals", "history"))));
  }
  const a = analyze({ uses, history, skills, asOf });
  const out = resolve(opt("--out", join(personal, isDemo ? "skill-health-sample.html" : "skill-health.html")));
  mkdirSync(dirname(out), { recursive: true });
  writeFileSync(out, render(a, { sample: isDemo }));
  writeFileSync(out.replace(/\.html$/, ".json"), JSON.stringify(a, null, 1));
  console.log(`${a.rows.length} skills · right first try ${pct(a.total.rate)} (${a.total.uses} uses, ${a.rules.recent_days} days) · ${a.needs.length} need you -> ${out}`);
  for (const n of a.needs) console.log(`  ${n.verdict.padEnd(7)} ${n.skill}: ${n.why}`);
}
