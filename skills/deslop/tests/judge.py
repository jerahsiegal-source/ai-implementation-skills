#!/usr/bin/env python3
"""Blind judge: deslop vs plain Claude on the AI fixtures.

The linter can't be the only referee, because deslop is built to satisfy it.
This asks a fresh model with no skills to compare the two rewrites, shuffled
as A and B, in both orders. A win counts only if it holds in both orders.

  python3 tests/judge.py --runs tests/runs/<run> [--model opus] [--jobs 6]

Writes <run>/blind/verdicts.json; run_tests.py adds it to report.md.
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")

PROMPT = """You are judging two edits of the same AI-written draft. The goal of each edit was: make it read clearly like a careful person wrote it, cut the fluff, and keep the same detail and information quality. It must never invent facts. Marking a missing detail for the author to fill in is allowed and is better than guessing.

ORIGINAL ({context}):
<original>
{original}
</original>

EDIT A:
<a>
{a}
</a>

EDIT B:
<b>
{b}
</b>

Score each edit 1 to 10 on:
- human: reads like a careful person wrote it, not a model
- variety: sentence length and structure vary naturally, no repeated templates
- lean: no fluff, filler, restating or long titles and subtitles
- specific: says concrete things, or clearly marks what is missing, instead of vague claims
- faithful: keeps every fact, number, name and useful detail from the original and adds none
Then pick the edit you would rather send, or "tie".

Reply with only JSON: {{"a": {{"human": n, "variety": n, "lean": n, "specific": n, "faithful": n}}, "b": {{"human": n, "variety": n, "lean": n, "specific": n, "faithful": n}}, "winner": "A" | "B" | "tie", "why": "one sentence"}}"""


def ask(prompt, model):
    cmd = ["claude", "-p", prompt, "--output-format", "json", "--disallowedTools", "Bash,Read,Write,Edit,Glob,Grep,WebFetch,WebSearch,Skill"]
    if model:
        cmd += ["--model", model]
    p = subprocess.run(cmd, cwd=os.path.expanduser("~"), capture_output=True, text=True, timeout=600, encoding="utf-8")
    out = json.loads(p.stdout).get("result", "")
    m = re.search(r"\{.*\}", out, re.S)
    return json.loads(m.group())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True)
    ap.add_argument("--model", default="")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--arm", default="deslop", help="skill arm folder inside --runs")
    ap.add_argument("--vs", default="", help="folder to compare against (default <runs>/baseline)")
    ap.add_argument("--out", default="verdicts.json", help="file name under <runs>/blind/")
    a = ap.parse_args()
    items = []
    for name in sorted(os.listdir(os.path.join(FIX, "ai"))):
        fid = name[:-3]
        d = os.path.join(a.runs, a.arm, name)
        b = os.path.join(a.vs or os.path.join(a.runs, "baseline"), name)
        if os.path.exists(d) and os.path.exists(b):
            items.append((fid, fid.split("-")[1], open(os.path.join(FIX, "ai", name), encoding="utf-8").read(),
                          open(d, encoding="utf-8").read(), open(b, encoding="utf-8").read()))

    def job(it, order):
        fid, ctx, orig, d, b = it
        first, second = (d, b) if order == 1 else (b, d)
        v = ask(PROMPT.format(context=ctx, original=orig, a=first, b=second), a.model)
        win = {"A": "deslop" if order == 1 else "plain", "B": "plain" if order == 1 else "deslop"}.get(v.get("winner"), "tie")
        ds, bs = (v["a"], v["b"]) if order == 1 else (v["b"], v["a"])
        return fid, order, {"winner": win, "deslop": ds, "plain": bs, "why": v.get("why", "")}

    res = {}
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for fu in cf.as_completed([ex.submit(job, it, o) for it in items for o in (1, 2)]):
            try:
                fid, order, v = fu.result()
                res.setdefault(fid, {})["order%d" % order] = v
                print("judged %-40s order %d -> %s" % (fid, order, v["winner"]))
            except Exception as e:
                print("FAIL", e)
    summary = {"deslop": 0, "plain": 0, "split_or_tie": 0}
    for fid, r in res.items():
        w = {r.get("order1", {}).get("winner"), r.get("order2", {}).get("winner")}
        r["result"] = w.pop() if len(w) == 1 and w <= {"deslop", "plain"} else "split_or_tie"
        summary[r["result"] if r["result"] in summary else "split_or_tie"] += 1
    means = {}
    for arm in ("deslop", "plain"):
        for k in ("human", "variety", "lean", "specific", "faithful"):
            xs = [r[o][arm][k] for r in res.values() for o in ("order1", "order2") if o in r and k in r[o][arm]]
            means["%s_%s" % (arm, k)] = round(sum(xs) / len(xs), 1) if xs else None
    os.makedirs(os.path.join(a.runs, "blind"), exist_ok=True)
    with open(os.path.join(a.runs, "blind", a.out), "w") as f:
        json.dump({"arm": a.arm, "vs": a.vs or "baseline", "summary": summary, "means": means, "verdicts": res}, f, indent=1)
    print(json.dumps({"summary": summary, "means": means}, indent=1))


if __name__ == "__main__":
    sys.exit(main())
