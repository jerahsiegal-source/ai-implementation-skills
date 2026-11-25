#!/usr/bin/env python3
"""Does my-voice beat plain Claude? A blind test with your own writing as the answer key.

You pick real messages you wrote (held out), and write a short fact-only brief
for each. Every arm drafts the same briefs; a fresh judge with no skills then
compares the drafts with what you actually sent.

Arms:
  plain         plain Claude, given only the brief and your name
  samples       plain Claude plus all your other real samples pasted in
  voice         /my-voice draft, profile only (no deslop installed)
  voice_lint    /my-voice draft with deslop installed (lint final check)
  voice_deslop  the voice draft, then a full /deslop pass (mode=embedded)
  alt_<arm>     the same arm with --alt-skill (e.g. last version vs this one)

Judges (all blind, A/B shuffled):
  turing   real message vs draft, both orders: "which did the person write?"
           fooled = the judge picked the draft. 50% means indistinguishable.
  rubric   all drafts for a task at once, shuffled, next to the real message:
           voice match 1-10, invented facts (count), would-send 1-10.

Everything is read from and written to the private data folder:
  <home>/evals/tasks.json   [{"id": "e07", "medium": "email", "real": "E7",
                              "brief": "To a client ... facts only"}]
  <home>/evals/runs/<date>-<runner>-<model>/...
Held-out samples are stripped from a temp copy of the corpus before drafting,
so no arm can read the answer.

  python3 tests/voice_eval.py run   [--arms plain,voice] [--model opus] [--jobs 6]
  python3 tests/voice_eval.py judge --run <run folder>
  python3 tests/voice_eval.py report --run <run folder>

Re-run when a new model comes out. Use --runner codex for Codex.
"""
import argparse
import concurrent.futures as cf
import datetime
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import voice  # noqa: E402

ARMS = ["plain", "samples", "voice", "voice_lint", "voice_deslop"]
CONTEXT = {"email": "email", "text": "general", "chat": "general", "social": "social",
           "report": "report", "resume": "resume"}
HEAD = re.compile(r"^## ([A-Z]+\d+) \|.*$", re.M)


# ---------- corpus helpers ----------

def split_samples(text):
    """Return [(id, header_line, body)] for '## ID | ...' sections."""
    out, marks = [], list(HEAD.finditer(text))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        out.append((m.group(1), m.group(0), text[m.end():end].strip().rstrip("-").strip()))
    return out


def real_text(home, sid):
    for root, _, files in os.walk(os.path.join(home, "corpus", "samples")):
        for f in files:
            if f.endswith(".md"):
                for i, _, body in split_samples(open(os.path.join(root, f), encoding="utf-8").read()):
                    if i == sid:
                        return re.sub(r"^Context:.*\n+", "", body).strip()
    sys.exit(f"sample {sid} not found")


def sanitized_home(home, held_out, dest):
    """Copy home without evals/, versions/ and held-out sample sections."""
    shutil.copytree(home, dest, ignore=shutil.ignore_patterns("evals", "versions", "blindtest"))
    for root, _, files in os.walk(os.path.join(dest, "corpus", "samples")):
        for f in files:
            p = os.path.join(root, f)
            if not f.endswith(".md"):
                continue
            text = open(p, encoding="utf-8").read()
            for sid, head, body in split_samples(text):
                if sid in held_out:
                    text = text.replace(head, f"## {sid} | (held out for testing)", 1).replace(body, "", 1)
            open(p, "w", encoding="utf-8").write(text)
    for root, _, files in os.walk(os.path.join(dest, "profile")):
        for f in files:
            body = open(os.path.join(root, f), encoding="utf-8").read()
            hits = [s for s in held_out if re.search(r"\b%s\b" % s, body)]
            if hits:
                print(f"note: profile/{f} cites held-out {', '.join(hits)}; pick other samples for a cleaner test")
    return dest


def samples_pack(shome, limit_words=12000, per_file=None):
    parts, n = [], 0
    for f in sorted(os.listdir(os.path.join(shome, "corpus", "samples"))):
        p = os.path.join(shome, "corpus", "samples", f)
        if not f.endswith(".md") or f == "index.md":
            continue
        start = n
        for sid, head, body in split_samples(open(p, encoding="utf-8").read()):
            if per_file and n - start > per_file:
                break
            low = head.lower()
            if "held out" in low or "ai-written" in low or "someone else" in low or "ai-assisted" in low or not body:
                continue
            w = len(body.split())
            if n + w > limit_words:
                break
            parts.append(f"{head}\n{body}")
            n += w
    return "\n\n".join(parts)


# ---------- runners ----------

def call(runner, model, prompt, cwd, env=None, tools=True, timeout=900):
    t0 = time.time()
    if runner == "claude":
        cmd = ["claude", "-p", prompt, "--output-format", "json"]
        if tools:
            cmd += ["--allowedTools", "Bash", "Read", "Write", "Edit", "Skill", "Glob", "Grep"]
        else:
            cmd += ["--disallowedTools", "Bash,Read,Write,Edit,Glob,Grep,WebFetch,WebSearch,Skill,Agent,Task"]
        if model:
            cmd += ["--model", model]
    else:
        cmd = ["codex", "exec", "--skip-git-repo-check", "--full-auto", prompt]
        if model:
            cmd += ["-m", model]
    p = subprocess.run(cmd, cwd=cwd, env={**os.environ, **(env or {})}, capture_output=True,
                       text=True, timeout=timeout, encoding="utf-8")
    out, cost = p.stdout, None
    if runner == "claude":
        try:
            j = json.loads(p.stdout)
            out, cost = j.get("result", ""), j.get("total_cost_usd")
        except ValueError:
            pass
    return out.strip(), {"seconds": round(time.time() - t0, 1), "usd": cost}


def install(workdir, names, deslop_dir, skill=SKILL):
    for d in (".claude/skills", ".agents/skills"):
        os.makedirs(os.path.join(workdir, d), exist_ok=True)
        for name in names:
            src = skill if name == "my-voice" else deslop_dir
            dest = os.path.join(workdir, d, name)
            try:
                os.symlink(src, dest, target_is_directory=True)
            except OSError:
                shutil.copytree(src, dest, ignore=shutil.ignore_patterns("tests", "runs"))


def clean_block(text):
    m = re.search(r"CLEAN TEXT:\s*\n(.*?)(?:\n\s*NEEDS YOUR INPUT|\Z)", text, re.S)
    return (m.group(1) if m else text).strip()


ONLY = ("Reply with only the message, exactly as it would be sent: no preamble, no notes, "
        "no code fences.")


def gen(arm, task, a, shome, author, pack, outdir):
    medium, brief = task["medium"], task["brief"]
    skill = SKILL
    if arm.startswith("alt_"):  # same arm, older or other copy of the skill (--alt-skill)
        arm, skill = arm[4:], a.alt_skill
    work = tempfile.mkdtemp(prefix="mv-")
    env = {"MY_VOICE_HOME": shome}
    if arm == "plain":
        prompt = f"Write this {medium} as {author}.\n\n{brief}\n\n{ONLY}"
        return call(a.runner, a.model, prompt, work, tools=False)
    if arm == "samples":
        prompt = (f"Here are real messages {author} wrote:\n\n<samples>\n{pack}\n</samples>\n\n"
                  f"Write this {medium} as {author}, in the same voice.\n\n{brief}\n\n{ONLY}")
        return call(a.runner, a.model, prompt, work, tools=False)
    if arm in ("voice", "voice_lint"):
        install(work, ["my-voice"] + (["deslop"] if arm == "voice_lint" else []), a.deslop, skill)
        prompt = f"/my-voice draft a {medium}\n\n{brief}\n\n{ONLY}"
        return call(a.runner, a.model, prompt, work, env)
    if arm == "voice_deslop":
        src = os.path.join(outdir, "voice", task["id"] + ".md")
        if not os.path.exists(src):
            raise RuntimeError("run the voice arm first")
        install(work, ["deslop"], a.deslop)
        shutil.copy(src, os.path.join(work, "input.md"))
        prompt = (f"/deslop context={CONTEXT.get(medium, 'general')} mode=embedded\n\n"
                  "The text to clean is in input.md in the current folder.")
        out, cost = call(a.runner, a.model, prompt, work, env)
        return clean_block(out), cost
    raise ValueError(arm)


def cmd_run(a):
    home = a.home
    tasks = json.load(open(os.path.join(home, "evals", "tasks.json"), encoding="utf-8"))
    author = a.author or "the author"
    held = {t["real"] for t in tasks}
    tag = f"{datetime.date.today()}-{a.runner}-{a.model or 'default'}"
    outdir = a.run or os.path.join(home, "evals", "runs", tag)
    os.makedirs(outdir, exist_ok=True)
    shome = sanitized_home(home, held, os.path.join(tempfile.mkdtemp(prefix="mvhome-"), "home"))
    pack = samples_pack(shome)
    arms = a.arms.split(",")
    costs_p = os.path.join(outdir, "costs.json")
    costs = json.load(open(costs_p)) if os.path.exists(costs_p) else {}

    def job(arm, t):
        out, cost = gen(arm, t, a, shome, author, pack, outdir)
        os.makedirs(os.path.join(outdir, arm), exist_ok=True)
        open(os.path.join(outdir, arm, t["id"] + ".md"), "w", encoding="utf-8").write(out + "\n")
        return arm, t["id"], cost

    for stage in ([x for x in arms if x != "voice_deslop"], [x for x in arms if x == "voice_deslop"]):
        with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
            futs = [ex.submit(job, arm, t) for arm in stage for t in tasks]
            for fu in cf.as_completed(futs):
                try:
                    arm, tid, cost = fu.result()
                    costs[f"{tid}/{arm}"] = cost
                    print(f"drafted {tid:<8} {arm:<13} {cost}")
                except Exception as e:  # keep going
                    print("FAIL", e)
    json.dump(costs, open(costs_p, "w"), indent=1)
    print(f"\nrun folder: {outdir}\nnext: python3 tests/voice_eval.py judge --run \"{outdir}\"")


# ---------- judge ----------

TURING = """Below are short samples of one person's real writing, then two messages for the same situation. One message was written by that person. The other was written by an AI imitating them from a brief.

<their_writing>
{ref}
</their_writing>

Situation (the facts both writers were given): {brief}

MESSAGE A:
<a>
{a}
</a>

MESSAGE B:
<b>
{b}
</b>

Which message did the person actually write? Reply with only JSON: {{"real": "A" | "B", "confidence": 1-5, "tell": "a few words on what gave the AI away"}}"""

RUBRIC = """You are grading AI drafts that try to write in one person's voice. Here is the brief the drafters got, and the message the person actually sent for this situation (the answer key for style; the drafters never saw it).

BRIEF: {brief}

THE PERSON'S REAL MESSAGE:
<real>
{real}
</real>

DRAFTS:
{drafts}

For each draft, score:
- voice: 1-10, how much it reads like the same person wrote it (tone, length, greeting, word choice, punctuation, formality), compared with the real message
- invented: number of facts, events, excuses, numbers or commitments in the draft that are NOT in the brief
- send: 1-10, how likely the person would send it as is

Reply with only JSON: {{"scores": {{"<draft number>": {{"voice": n, "invented": n, "send": n}}}}, "best": "<draft number>", "why": "one sentence"}}"""


def ask_json(prompt, a):
    out, _ = call(a.runner, a.judge_model or a.model, prompt, os.path.expanduser("~"), tools=False, timeout=600)
    m = re.search(r"\{.*\}", out, re.S)
    return json.loads(m.group())


def strip_subject(text):
    """Samples are stored without subject lines, so drafts are judged without them too."""
    return re.sub(r"^\s*Subject:.*\n+", "", text.strip()).strip()


def reference_pack(home, held, words=900):
    shome = sanitized_home(home, held, os.path.join(tempfile.mkdtemp(prefix="mvref-"), "home"))
    return samples_pack(shome, words, per_file=words // 4)


def cmd_judge(a):
    home, run = a.home, a.run
    tasks = json.load(open(os.path.join(home, "evals", "tasks.json"), encoding="utf-8"))
    held = {t["real"] for t in tasks}
    ref = reference_pack(home, held)
    arms = [x for x in sorted(os.listdir(run)) if os.path.isdir(os.path.join(run, x))]
    rng = random.Random(7)
    jobs = []
    for t in tasks:
        real = real_text(home, t["real"])
        drafts = {arm: strip_subject(open(os.path.join(run, arm, t["id"] + ".md"), encoding="utf-8").read())
                  for arm in arms if os.path.exists(os.path.join(run, arm, t["id"] + ".md"))}
        for arm, d in drafts.items():
            for order in (1, 2):
                A, B = (real, d) if order == 1 else (d, real)
                jobs.append(("turing", t["id"], arm, order,
                             TURING.format(ref=ref, brief=t["brief"], a=A, b=B)))
        for rep in (1, 2):
            names = list(drafts)
            rng.shuffle(names)
            block = "\n\n".join(f"DRAFT {i + 1}:\n<draft>\n{drafts[n]}\n</draft>" for i, n in enumerate(names))
            jobs.append(("rubric", t["id"], names, rep,
                         RUBRIC.format(brief=t["brief"], real=real, drafts=block)))

    res = {"turing": {}, "rubric": {}}

    def do(j):
        kind, tid, arm, order, prompt = j
        return j, ask_json(prompt, a)

    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for fu in cf.as_completed([ex.submit(do, j) for j in jobs]):
            try:
                (kind, tid, arm, order, _), v = fu.result()
            except Exception as e:
                print("FAIL", e)
                continue
            if kind == "turing":
                fooled = (v.get("real") == "B") if order == 1 else (v.get("real") == "A")
                res["turing"].setdefault(tid, {}).setdefault(arm, []).append(
                    {"fooled": fooled, "conf": v.get("confidence"), "tell": v.get("tell", "")})
                print(f"turing {tid:<8} {arm:<13} order {order} fooled={fooled}")
            else:
                names = arm
                per = {names[int(k) - 1]: s for k, s in v.get("scores", {}).items() if k.isdigit() and int(k) <= len(names)}
                best = v.get("best")
                res["rubric"].setdefault(tid, []).append(
                    {"scores": per, "best": names[int(best) - 1] if str(best).isdigit() and int(best) <= len(names) else None,
                     "why": v.get("why", "")})
                print(f"rubric {tid:<8} rep {order} best={res['rubric'][tid][-1]['best']}")
    json.dump(res, open(os.path.join(run, "verdicts.json"), "w"), indent=1)
    cmd_report(a)


def cmd_report(a):
    run = a.run
    res = json.load(open(os.path.join(run, "verdicts.json")))
    costs = json.load(open(os.path.join(run, "costs.json"))) if os.path.exists(os.path.join(run, "costs.json")) else {}
    arms = sorted({arm for t in res["turing"].values() for arm in t},
                  key=lambda x: (ARMS.index(x.replace("alt_", "")) if x.replace("alt_", "") in ARMS else 99, x))
    rows = {}
    for arm in arms:
        f = [x["fooled"] for t in res["turing"].values() for x in t.get(arm, [])]
        sc = [r["scores"][arm] for reps in res["rubric"].values() for r in reps if arm in r["scores"]]
        best = sum(1 for reps in res["rubric"].values() for r in reps if r["best"] == arm)
        usd = [c["usd"] for k, c in costs.items() if k.endswith("/" + arm) and c and c.get("usd")]
        mean = lambda k: round(sum(s.get(k, 0) for s in sc) / len(sc), 1) if sc else None  # noqa: E731
        rows[arm] = {"fooled_pct": round(100 * sum(f) / len(f)) if f else None, "turing_n": len(f),
                     "voice": mean("voice"), "send": mean("send"), "invented": mean("invented"),
                     "best_count": best, "usd_per_draft": round(sum(usd) / len(usd), 3) if usd else None}
    json.dump(rows, open(os.path.join(run, "summary.json"), "w"), indent=1)
    print("\narm            fooled  voice  send  invented  best  $/draft")
    for arm, r in rows.items():
        print(f"{arm:<14} {str(r['fooled_pct']) + '%':>6}  {r['voice']!s:>5}  {r['send']!s:>4}  {r['invented']!s:>8}  {r['best_count']:>4}  {r['usd_per_draft']}")
    print(f"\n(fooled: judge picked the draft as the real message; 50% = can't tell them apart)\nsaved {os.path.join(run, 'summary.json')}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["run", "judge", "report"])
    ap.add_argument("--home", default=str(voice.home()))
    ap.add_argument("--run", default="")
    ap.add_argument("--arms", default=",".join(ARMS))
    ap.add_argument("--author", default="", help="name the plain arm writes as")
    ap.add_argument("--runner", default="claude", choices=["claude", "codex"])
    ap.add_argument("--model", default="")
    ap.add_argument("--judge-model", default="")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--alt-skill", default="", help="another copy of my-voice for alt_<arm> arms (e.g. the last version)")
    ap.add_argument("--deslop", default=os.path.join(os.path.dirname(SKILL), "deslop"),
                    help="path to the deslop skill folder")
    a = ap.parse_args()
    if a.cmd != "run" and not a.run:
        sys.exit("--run <folder> is required")
    {"run": cmd_run, "judge": cmd_judge, "report": cmd_report}[a.cmd](a)


if __name__ == "__main__":
    main()
