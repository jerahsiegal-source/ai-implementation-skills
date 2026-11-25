#!/usr/bin/env python3
"""Run deslop and plain Claude (or Codex) on every fixture and save the outputs.

Each fixture runs three ways:
  deslop    the skill, once         (tests the rewrite)
  deslop2   the skill on its own output (tests idempotence)
  review    any other arm name runs the current skill too (e.g. after adding a step)
  workloop  the work-loop skill driving deslop mode=rewrite (INTENT.md per sample)
  baseline  the same ask with no skill installed (does the skill beat plain Claude?)

  python3 tests/run_live.py                      # claude -p, default model
  python3 tests/run_live.py --model sonnet --jobs 6
  python3 tests/run_live.py --mode rewrite --only a --arms deslop   # opt-in rewrite mode
  python3 tests/run_live.py --runner codex       # codex exec
  python3 tests/run_live.py --only a06,h10 --arms deslop

Outputs go to tests/runs/<date>-<runner>-<model>/<arm>/<fixture>.md with
costs.json ({"<fixture>/<arm>": {"tokens": n, "seconds": n}}). Then run
python3 tests/run_tests.py --runs <that folder>. Re-run when a new model
comes out, in both Claude Code and Codex.
"""
import argparse
import concurrent.futures as cf
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
FIX = os.path.join(HERE, "fixtures")

BASELINE_PROMPT = (
    "Rewrite this {context} text so it doesn't read as AI-written. Keep every fact. "
    "Reply with only the rewritten text.\n\n<text>\n{text}\n</text>"
)
SKILL_PROMPT = (
    "/deslop context={context} {mode}mode=embedded\n\n"
    "The text to clean is in input.md in the current folder."
)


def fixtures(only=None):
    out = []
    for kind in ("ai", "human"):
        for name in sorted(os.listdir(os.path.join(FIX, kind))):
            if not name.endswith(".md"):
                continue
            fid = name[:-3]
            if only and not any(fid.startswith(o) for o in only):
                continue
            ctx = fid.split("-")[1]
            out.append((kind, fid, ctx, os.path.join(FIX, kind, name)))
    return out


def install_skill(workdir, names=("deslop",)):
    for d in (".claude/skills", ".agents/skills"):
        os.makedirs(os.path.join(workdir, d), exist_ok=True)
        for name in names:
            src = os.path.join(os.path.dirname(SKILL), name)
            dest = os.path.join(workdir, d, name)
            try:
                os.symlink(src, dest, target_is_directory=True)
            except OSError:
                shutil.copytree(src, dest, ignore=shutil.ignore_patterns("runs", "fixtures"))


WORKLOOP_INTENT = """# Rewrite input.md so it reads like a person wrote it

## Outcome
output.md holds input.md ({context} text) rewritten with `/deslop context={context} mode=rewrite`, so a reader would take it for a careful person's writing.

## Why
The draft is AI-written. Stripping tells is not enough; it has to read clearly human and better.

## Done when (all must pass)
- D1 `python3 .claude/skills/deslop/scripts/lint.py output.md --context {context} --max-high 0` exits 0.
- D2 `python3 .claude/skills/deslop/scripts/facts.py input.md output.md --text` exits 0.
- D3 A fresh reviewer given only input.md, output.md and .claude/skills/deslop/references/reader-check.md returns VERDICT: PASS.
- D4 Every title is a few plain words, with no subtitle.

## Never
- Invent a fact, number, name or detail. Use [NEEDS SPECIFIC: ...] instead.
- Change code, URLs or quotes.

## Yours to decide
- Wording, sentence order inside a paragraph, which fluff to cut.

## Stop and ask before
- Nothing. No PR, no push, no deploy.
"""
WORKLOOP_PROMPT = ("/work-loop INTENT.md\n\nThis is a small text job in a scratch folder: skip the branch, baseline "
                   "and PR steps, keep the check, review and fix loop. When done, reply with only the contents of output.md.")


def call(runner, model, prompt, workdir, timeout):
    t0 = time.time()
    if runner == "claude":
        cmd = ["claude", "-p", prompt, "--output-format", "json",
               "--allowedTools", "Bash", "Read", "Write", "Edit", "Skill", "Agent", "Task", "Glob", "Grep"]
        if model:
            cmd += ["--model", model]
    else:
        cmd = ["codex", "exec", "--skip-git-repo-check", "--full-auto", prompt]
        if model:
            cmd += ["-m", model]
    p = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True, timeout=timeout,
                       encoding="utf-8")
    secs = round(time.time() - t0, 1)
    tokens = None
    out = p.stdout
    if runner == "claude":
        try:
            j = json.loads(p.stdout)
            out = j.get("result", "")
            u = j.get("usage", {})
            tokens = sum(u.get(k, 0) or 0 for k in ("input_tokens", "output_tokens",
                                                     "cache_creation_input_tokens", "cache_read_input_tokens"))
            secs = (secs, j.get("total_cost_usd"))  # cost includes subagents
        except json.JSONDecodeError:
            pass
    if p.returncode != 0 and not out.strip():
        raise RuntimeError("runner failed: %s" % (p.stderr[-500:] or p.stdout[-500:]))
    return out, secs, tokens


def clean_block(reply):
    """Pull the CLEAN TEXT block out of an embedded-mode reply."""
    m = re.search(r"CLEAN TEXT:\s*\n(.*?)(?:\n\s*NEEDS YOUR INPUT|\Z)", reply, re.S)
    text = m.group(1) if m else reply
    text = text.strip("\n")
    # strip a wrapping code fence if the model added one around the whole text
    f = re.fullmatch(r"\s*```[\w-]*\n(.*?)\n```\s*", text, re.S)
    if f and "```" not in f.group(1):
        text = f.group(1)
    return text.rstrip() + "\n"


def run_one(arm, runner, model, ctx, text, timeout, mode=""):
    with tempfile.TemporaryDirectory(prefix="deslop-%s-" % arm) as wd:
        if arm == "baseline":
            prompt = BASELINE_PROMPT.format(context=ctx, text=text)
            out, secs, tokens = call(runner, model, prompt, wd, timeout)
            return out.strip() + "\n", secs, tokens
        if arm == "workloop":
            install_skill(wd, ("deslop", "work-loop"))
            with open(os.path.join(wd, "input.md"), "w", encoding="utf-8") as f:
                f.write(text)
            with open(os.path.join(wd, "INTENT.md"), "w", encoding="utf-8") as f:
                f.write(WORKLOOP_INTENT.format(context=ctx))
            out, secs, tokens = call(runner, model, WORKLOOP_PROMPT, wd, timeout)
            op = os.path.join(wd, "output.md")
            return (open(op, encoding="utf-8").read() if os.path.exists(op) else clean_block(out)), secs, tokens
        install_skill(wd)
        with open(os.path.join(wd, "input.md"), "w", encoding="utf-8") as f:
            f.write(text)
        out, secs, tokens = call(runner, model, SKILL_PROMPT.format(context=ctx, mode=("mode=%s " % mode) if mode else ""), wd, timeout)
        return clean_block(out), secs, tokens


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runner", choices=["claude", "codex"], default="claude")
    ap.add_argument("--model", default="")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--only", default="", help="comma-separated fixture id prefixes")
    ap.add_argument("--arms", default="deslop,deslop2,baseline")
    ap.add_argument("--out", default="")
    ap.add_argument("--mode", default="", help="extra skill mode for the deslop arms, e.g. rewrite")
    ap.add_argument("--timeout", type=int, default=600)
    a = ap.parse_args()
    arms = a.arms.split(",")
    only = [o for o in a.only.split(",") if o]
    label = "%s-%s-%s" % (datetime.date.today().isoformat(), a.runner, a.model or "default")
    out_dir = a.out or os.path.join(HERE, "runs", label)
    for arm in arms:
        os.makedirs(os.path.join(out_dir, arm), exist_ok=True)
    cost_path = os.path.join(out_dir, "costs.json")
    costs = json.load(open(cost_path)) if os.path.exists(cost_path) else {}
    fx = fixtures(only)

    def job(item, arm):
        kind, fid, ctx, path = item
        src = path
        if arm == "deslop2":
            src = os.path.join(out_dir, "deslop", fid + ".md")
        with open(src, encoding="utf-8") as f:
            text = f.read()
        out, secs, tokens = run_one(arm, a.runner, a.model, ctx, text, a.timeout, a.mode)
        with open(os.path.join(out_dir, arm, fid + ".md"), "w", encoding="utf-8") as f:
            f.write(out)
        return fid, arm, secs, tokens

    def run_arms(arm_list):
        with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
            futs = [ex.submit(job, item, arm) for arm in arm_list for item in fx]
            for fu in cf.as_completed(futs):
                try:
                    fid, arm, secs, tokens = fu.result()
                    usd = None
                    if isinstance(secs, tuple):
                        secs, usd = secs
                    costs["%s/%s" % (fid, arm)] = {"tokens": tokens, "seconds": secs, "usd": usd}
                    print("ok   %-40s %-8s %6.1fs %s tokens $%s" % (fid, arm, secs, tokens, usd))
                except Exception as e:  # keep going; report at the end
                    print("FAIL %s" % e)
        with open(cost_path, "w") as f:
            json.dump(costs, f, indent=1, sort_keys=True)

    run_arms([x for x in arms if x != "deslop2"])
    if "deslop2" in arms:
        run_arms(["deslop2"])
    meta = {"runner": a.runner, "model": a.model or "default", "date": datetime.date.today().isoformat(),
            "fixtures": len(fx), "arms": arms, "mode": a.mode or "default"}
    with open(os.path.join(out_dir, "meta.json"), "w") as f:
        json.dump(meta, f, indent=1)
    print("\nSaved to %s\nNext: python3 tests/run_tests.py --runs %s" % (out_dir, out_dir))


if __name__ == "__main__":
    sys.exit(main())
