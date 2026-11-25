#!/usr/bin/env python3
"""Does /deslop learn actually learn? A live test with a simulated user.

A scripted editor with three fixed habits edits deslop's drafts of a few
training samples into "finals". deslop learns from those pairs in a throwaway
private folder. Then deslop rewrites held-out samples with and without the
learned preferences, and a grader counts how often each version breaks the
editor's habits. Learning works if the count drops and no fact is lost.

  python3 tests/run_learning.py --runs tests/runs/<run with a review2 arm>

Writes <runs>/learning/ (finals, learned preferences, outputs, result.json).
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scripts"))
import run_live  # noqa: E402
import facts  # noqa: E402

HABITS = """1. No titles or headings of any kind (no markdown headings, no bold title lines). A "Subject:" line in an email is fine.
2. Never end with a sentence that promises follow-up or offers help ("we'll keep you posted", "let me know if...", "happy to...", "we'll come back to you").
3. No bullet or numbered lists: write the items as plain sentences in a paragraph. Tables are fine."""

EDITOR = """You are editing a colleague's draft before it goes out. You have exactly these habits:
{habits}
Apply every habit everywhere it applies, every time. Change nothing else: same facts, same wording elsewhere, keep any [NEEDS SPECIFIC: ...] markers. Reply with only the edited text.

<draft>
{draft}
</draft>"""

GRADER = """Count how many times this text breaks each rule. Rules:
{habits}

<text>
{text}
</text>

Reply with only JSON: {{"1": n, "2": n, "3": n}}"""

# Training drafts and held-out drafts both break the habits, so there is something to learn and room to improve.
TRAIN = ["a07-report-billing-status", "a06-report-support-q3", "a09-email-dashboard-delay", "a03-email-coverletter-ux"]
HELD = ["a08-email-kickoff-followup", "a17-email-coverletter-classic", "a05-social-lesson", "a04-social-launch", "a15-social-manager-classic"]


def ask(prompt, model=""):
    cmd = ["claude", "-p", prompt, "--output-format", "json", "--disallowedTools",
           "Bash,Read,Write,Edit,Glob,Grep,WebFetch,WebSearch,Skill"]
    if model:
        cmd += ["--model", model]
    p = subprocess.run(cmd, cwd=os.path.expanduser("~"), capture_output=True, text=True, timeout=600, encoding="utf-8")
    return json.loads(p.stdout).get("result", "").strip()


def grade(text, model=""):
    out = ask(GRADER.format(habits=HABITS, text=text), model)
    v = json.loads(re.search(r"\{.*\}", out, re.S).group())
    return {k: int(v.get(k, 0)) for k in ("1", "2", "3")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True, help="run folder with a review2 arm (drafts without learning)")
    ap.add_argument("--arm", default="review2")
    ap.add_argument("--model", default="")
    ap.add_argument("--confirm", action="store_true",
                    help="skip training: take <runs>/learning/preferences.md, mark every candidate confirmed "
                         "(as if the user said 'yes, those are right'), and re-test the held-out samples")
    a = ap.parse_args()
    out = os.path.join(a.runs, "learning")
    for d in ("finals", "with_prefs"):
        os.makedirs(os.path.join(out, d), exist_ok=True)
    personal = tempfile.mkdtemp(prefix="deslop-personal-")
    os.makedirs(os.path.join(personal, "deslop"))
    os.environ["AI_SKILLS_PERSONAL"] = personal  # every child process sees only this throwaway folder
    fix = os.path.join(HERE, "fixtures", "ai")
    learn_py = os.path.join(os.path.dirname(HERE), "scripts", "learn.py")
    costs = {}

    # 1. the simulated user edits deslop's drafts; deslop learns from each pair in turn
    if a.confirm:
        src = open(os.path.join(out, "preferences.md"), encoding="utf-8").read()
        rules, cands = src.split("## Candidates", 1)
        lines = [l.replace("[seen 1]", "[seen 1] confirmed") for l in cands.splitlines() if l.startswith("- ")]
        src = rules.rstrip() + "\n" + "\n".join(lines) + "\n\n## Candidates (seen once)\n"
        with open(os.path.join(personal, "deslop", "preferences.md"), "w", encoding="utf-8") as f:
            f.write(src)
        out = os.path.join(out, "confirmed")
        os.makedirs(os.path.join(out, "with_prefs"), exist_ok=True)
    for fid in ([] if a.confirm else TRAIN):
        ctx = fid.split("-")[1]
        orig = open(os.path.join(fix, fid + ".md"), encoding="utf-8").read()
        draft = open(os.path.join(a.runs, a.arm, fid + ".md"), encoding="utf-8").read()
        final = ask(EDITOR.format(habits=HABITS, draft=draft), a.model) + "\n"
        with open(os.path.join(out, "finals", fid + ".md"), "w", encoding="utf-8") as f:
            f.write(final)
        with tempfile.TemporaryDirectory() as wd:
            for n, t in (("original.md", orig), ("draft.md", draft), ("final.md", final)):
                with open(os.path.join(wd, n), "w", encoding="utf-8") as f:
                    f.write(t)
            subprocess.run([sys.executable, learn_py, "save", "--original", os.path.join(wd, "original.md"),
                            "--draft", os.path.join(wd, "draft.md"), "--context", ctx], check=True, capture_output=True)
            run_live.install_skill(wd)
            prompt = "/deslop learn\n\nHere's the version I actually sent, in final.md. It's my edit of the %s draft you gave me." % ctx
            reply, secs, tokens = run_live.call("claude", a.model, prompt, wd, 900)
            costs[fid + "/learn"] = {"seconds": secs if not isinstance(secs, tuple) else secs[0], "tokens": tokens}
            print("learned from", fid, "\n", reply[-600:], "\n")
    prefs = os.path.join(personal, "deslop", "preferences.md")
    shutil.copy(prefs, os.path.join(out, "preferences.md"))  # in --confirm mode this lands in learning/confirmed/

    # 2. held-out samples: deslop with the learned preferences
    rows = {}
    for fid in HELD:
        ctx = fid.split("-")[1]
        orig = open(os.path.join(fix, fid + ".md"), encoding="utf-8").read()
        new, secs, tokens = run_live.run_one("deslop", "claude", a.model, ctx, orig, 900, "rewrite")
        with open(os.path.join(out, "with_prefs", fid + ".md"), "w", encoding="utf-8") as f:
            f.write(new)
        old = open(os.path.join(a.runs, a.arm, fid + ".md"), encoding="utf-8").read()
        rows[fid] = {"without": grade(old, a.model), "with": grade(new, a.model),
                     "facts_ok_with": not facts.compare(orig, new)["hard_fail"]}
        print(fid, rows[fid])
    tot = lambda k: sum(sum(r[k].values()) for r in rows.values())  # noqa: E731
    res = {"habits": HABITS, "train": TRAIN, "held_out": HELD, "rows": rows,
           "habit_breaks_without": tot("without"), "habit_breaks_with": tot("with"),
           "facts_ok": all(r["facts_ok_with"] for r in rows.values()), "costs": costs}
    with open(os.path.join(out, "result.json"), "w") as f:
        json.dump(res, f, indent=1)
    print(json.dumps({k: res[k] for k in ("habit_breaks_without", "habit_breaks_with", "facts_ok")}))
    shutil.rmtree(personal, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
