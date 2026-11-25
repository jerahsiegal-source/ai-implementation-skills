#!/usr/bin/env python3
"""deslop tests. Stdlib only.

  python3 tests/run_tests.py                 # linter + fixture tests, and the newest saved run
  python3 tests/run_tests.py --runs <dir>    # check a run made by run_live.py
  python3 tests/run_tests.py --no-runs       # skip saved runs (CI)

Part 1 (always): the linter and fact checker work, rules match the reference
files, the linter tells the AI fixtures from the human ones.
Part 2 (with a run): the skill's rewrites raise scores, clear high hits, keep
facts and code, leave human text mostly alone, are idempotent, and are
compared with plain Claude on the same fixtures. Writes report.json and
report.md into the run folder.
"""
import argparse
import difflib
import glob
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import facts  # noqa: E402
import lint  # noqa: E402

FIX = os.path.join(HERE, "fixtures")
RESULTS = []

# Thresholds. Change them here, and say why in the commit.
HUMAN_MAX_HIGH = 0          # human fixtures: no high-severity hits
HUMAN_MIN_SIMILARITY = 0.85 # word-level similarity between human input and deslop output
HUMAN_MAX_MARKERS = 1       # [NEEDS SPECIFIC] markers allowed per human fixture
IDEMPOTENT_MIN = 0.95       # similarity between pass 1 and pass 2
AI_FLAGGED_SHARE = 0.75     # share of AI fixtures the linter must flag (score < 85 or any high)


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  (" + detail + ")") if detail else ""))
    return ok


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def fixtures():
    out = []
    for kind in ("ai", "human"):
        for p in sorted(glob.glob(os.path.join(FIX, kind, "*.md"))):
            fid = os.path.basename(p)[:-3]
            out.append((kind, fid, fid.split("-")[1], p))
    return out


def similarity(a, b):
    return difflib.SequenceMatcher(None, a.split(), b.split(), autojunk=False).ratio()


def strip_markers(t):
    return re.sub(r"\s*\[NEEDS SPECIFIC:[^\]]*\]", "", t)


def markers(t):
    return len(re.findall(r"\[NEEDS SPECIFIC:[^\]]*\]", t))


# ------------------------------------------------------------------ part 1

def unit_tests():
    L = lambda t, **k: lint.lint(t, **k)
    ids = lambda r: [h["id"] for h in r["hits"]]

    r = L("We delve into the tapestry of data.\n\n```\ndelve tapestry — robust\n```\n\nRun `delve --robust` or see https://x.com/delve-robust.")
    check("linter: flags vocabulary in prose", ids(r).count("W-02") == 2, str(ids(r)))
    check("linter: skips code blocks, inline code and URLs", all(h["line"] == 1 for h in r["hits"]), str([(h["id"], h["line"]) for h in r["hits"]]))

    r1 = L("We shipped it — and it worked. Then we rested — briefly.")
    r2 = L("We shipped it — and it worked. Then we rested — briefly.", allow_em_dash=True)
    check("linter: flags em dashes", ids(r1).count("F-01") == 2)
    check("linter: --allow-em-dash turns them off", "F-01" not in ids(r2))
    check("linter: date ranges are not em dashes", "F-01" not in ids(L("Manager, 2020 – 2024")))

    t = "- Spearheaded the launch\n- Leveraged analytics\n- Orchestrated the migration\n- Championed testing\n"
    rr, rg = L(t, context="resume"), L(t, context="general")
    s05 = [h for h in rr["hits"] if h["id"] == "S-05"]
    check("linter: resume escalates stock-verb bullet runs to high", s05 and s05[0]["severity"] == "high", str(s05))
    check("linter: first person is flagged only in resume", "S-14" in ids(L("I led the team.", context="resume")) and "S-14" not in ids(rg))

    e = L("Hi Sam,\n\n**Update:** the deploy moved.\n\n### Next\nThanks", context="email")
    check("linter: markdown in email is high", any(h["id"] == "F-08" and h["severity"] == "high" for h in e["hits"]))
    check("linter: chatbot leftovers are high", any(h["id"] == "P-02" and h["severity"] == "high" for h in L("Great question! I hope this helps.")["hits"]))
    check("linter: placeholders are flagged", any(h["id"] == "P-10" for h in L("Grew [metric] by [X%].")["hits"]))
    check("linter: own [NEEDS SPECIFIC] markers are ignored", not L("It improved [NEEDS SPECIFIC: delve robust tapestry?].")["hits"])
    check("linter: contrast frame", "S-02" in ids(L("It's not just a CRM, it's a growth engine.")))
    check("linter: size word with a number is fine", "W-08" not in ids(L("Revenue grew significantly, from $2M to $3M.")))
    check("linter: size word without a number is flagged", "W-08" in ids(L("Revenue grew significantly last year.")))
    clean = L("The deploy failed at 9:40 because the migration locked the users table. Maria rolled it back by 9:52. We will rerun it tonight with the lock timeout set to 5 seconds.")
    check("linter: plain specific text scores 100", clean["score"] == 100, str(clean["score"]))
    many = ("Moreover, our robust, seamless and holistic platform leverages cutting-edge tools. " * 3)
    check("linter: word clusters escalate", any(h["severity"] in ("medium", "high") and h["category"] == "words" for h in L(many)["hits"]))
    check("linter: output has the contract keys", set(r) >= {"context", "score", "counts_by_category", "hits"} and
          set(r["hits"][0]) >= {"id", "category", "severity", "line", "col", "match", "suggestion"})
    import contextlib, io
    with contextlib.redirect_stdout(io.StringIO()):
        code_hi = lint.main(["--max-high", "0"] + [os.path.join(FIX, "ai", "a15-social-manager-classic.md")])
        code_ok = lint.main(["--max-high", "99", os.path.join(FIX, "human", "h02-docs-site-tests.md")])
    check("linter: exit code 1 on high hits, 0 otherwise", code_hi == 1 and code_ok == 0)

    # facts
    o = "Cut response time from 5.1 to 3.4 hours with Priya Shah at Brightline. See https://a.example/x. Run `make test`.\n\n```\nnpm ci\n```\n"
    good = "Priya Shah at Brightline cut response time from 5.1 to 3.4 hours [NEEDS SPECIFIC: how?]. See https://a.example/x. Run `make test`.\n\n```\nnpm ci\n```\n"
    bad = "Priya cut response time to 3.4 hours at Brightline. See https://a.example/y.\n\n```\nnpm install\n```\n"
    g, b = facts.compare(o, good), facts.compare(o, bad)
    check("facts: a faithful rewrite passes", g["ok"] and g["markers_added"] == 1, json.dumps(g)[:200])
    check("facts: lost number, URL and changed code are caught",
          "5.1" in b["numbers"]["lost"] and b["urls"]["lost"] and b["code_blocks"]["changed"] and b["hard_fail"])
    check("facts: lost surname is reported", "Shah" in b["names"]["lost"])

    # every rule id is documented in a reference file
    rules = lint.load_rules()
    all_ids = [r["id"] for g in ("word_rules", "phrase_rules", "structure_rules") for r in rules[g]] + list(rules["checks"])
    refs = "".join(read(p) for p in glob.glob(os.path.join(SKILL, "references", "*.md")))
    missing = [i for i in all_ids if "## %s " % i not in refs]
    check("rules: every rule id has a section in references/", not missing, ", ".join(missing))
    check("rules: every context in contexts.md", all("`%s`" % c in read(os.path.join(SKILL, "references", "contexts.md")) for c in rules["contexts"]))


def fixture_lint_tests():
    fx = fixtures()
    ai = [(fid, lint.lint(read(p), context=c)) for k, fid, c, p in fx if k == "ai"]
    hu = [(fid, lint.lint(read(p), context=c)) for k, fid, c, p in fx if k == "human"]
    check("fixtures: 10+ AI and 10+ human samples", len(ai) >= 10 and len(hu) >= 10, "%d AI, %d human" % (len(ai), len(hu)))
    bad_h = [f for f, r in hu if r["counts_by_severity"]["high"] > HUMAN_MAX_HIGH]
    check("fixtures: human samples have no high-severity hits", not bad_h, ", ".join(bad_h))
    flagged = [f for f, r in ai if r["score"] < 85 or r["counts_by_severity"]["high"]]
    check("fixtures: linter flags most AI samples", len(flagged) / len(ai) >= AI_FLAGGED_SHARE,
          "%d of %d flagged" % (len(flagged), len(ai)))
    ma, mh = statistics.median(r["score"] for _, r in ai), statistics.median(r["score"] for _, r in hu)
    check("fixtures: human median score beats AI median by 25+", mh - ma >= 25, "human %d, AI %d" % (mh, ma))
    return {f: r["score"] for f, r in ai + hu}


# ------------------------------------------------------------------ part 2

def run_tests(run_dir, before):
    meta_p = os.path.join(run_dir, "meta.json")
    meta = json.load(open(meta_p)) if os.path.exists(meta_p) else {}
    costs_p = os.path.join(run_dir, "costs.json")
    costs = json.load(open(costs_p)) if os.path.exists(costs_p) else {}
    rows = []
    for kind, fid, ctx, p in fixtures():
        src = read(p)
        row = {"fixture": fid, "kind": kind, "context": ctx, "before": before[fid]}
        for arm in ("deslop", "deslop2", "baseline"):
            op = os.path.join(run_dir, arm, fid + ".md")
            if not os.path.exists(op):
                continue
            out = read(op)
            ref = read(os.path.join(run_dir, "deslop", fid + ".md")) if arm == "deslop2" else src
            lr = lint.lint(out, context=ctx)
            fr = facts.compare(src if arm != "deslop2" else ref, out)
            row[arm] = {
                "score": lr["score"], "high": lr["counts_by_severity"]["high"],
                # pass 2 is compared with markers stripped: a new question is reported, not counted as churn
                "similarity": round(similarity(strip_markers(ref), strip_markers(out)) if arm == "deslop2" else similarity(ref, out), 3),
                "markers": markers(out),
                "facts_hard_fail": fr["hard_fail"], "lost_numbers": fr["numbers"]["lost"],
                "added_numbers": fr["numbers"]["added"], "lost_names": fr["names"]["lost"],
                "added_names": fr["names"]["added"], "code_changed": fr["code_blocks"]["changed"],
                "tokens": (costs.get("%s/%s" % (fid, arm)) or {}).get("tokens"),
                "seconds": (costs.get("%s/%s" % (fid, arm)) or {}).get("seconds"),
            }
        rows.append(row)

    have = [r for r in rows if "deslop" in r]
    if not have:
        check("run: outputs found", False, run_dir)
        return
    ai = [r for r in have if r["kind"] == "ai"]
    hu = [r for r in have if r["kind"] == "human"]
    rise = [r["fixture"] for r in ai if r["deslop"]["score"] < r["before"]]
    check("run: AI scores rise (or stay) after deslop", not rise, ", ".join(rise))
    hi = [r["fixture"] for r in ai if r["deslop"]["high"] > 0]
    check("run: no high-severity hits left in AI rewrites", not hi, ", ".join(hi))
    lost = [r["fixture"] for r in have if r["deslop"]["facts_hard_fail"]]
    check("run: numbers, URLs and code kept in every rewrite", not lost,
          "; ".join("%s lost %s added %s" % (r["fixture"], r["deslop"]["lost_numbers"], r["deslop"]["added_numbers"]) for r in have if r["deslop"]["facts_hard_fail"]))
    code = [r["fixture"] for r in have if r["deslop"]["code_changed"]]
    check("run: code blocks untouched", not code, ", ".join(code))
    ed = [("%s %.2f" % (r["fixture"], r["deslop"]["similarity"])) for r in hu if r["deslop"]["similarity"] < HUMAN_MIN_SIMILARITY]
    check("run: human text mostly untouched (similarity >= %.2f)" % HUMAN_MIN_SIMILARITY, not ed, ", ".join(ed))
    spam = [r["fixture"] for r in hu if r["deslop"]["markers"] > HUMAN_MAX_MARKERS]
    check("run: no [NEEDS SPECIFIC] spam on human text", not spam, ", ".join(spam))
    idem = [r for r in have if "deslop2" in r]
    if idem:
        bad = ["%s %.2f" % (r["fixture"], r["deslop2"]["similarity"]) for r in idem if r["deslop2"]["similarity"] < IDEMPOTENT_MIN]
        check("run: idempotent (second pass prose similarity >= %.2f)" % IDEMPOTENT_MIN, not bad, ", ".join(bad))
        more = ["%s +%d" % (r["fixture"], r["deslop2"]["markers"] - r["deslop"]["markers"]) for r in idem if r["deslop2"]["markers"] > r["deslop"]["markers"]]
        print("      note: second pass added markers on %d samples%s" % (len(more), (": " + ", ".join(more)) if more else ""))

    # comparison with plain Claude: reported, not pass/fail
    def mean(xs):
        xs = [x for x in xs if x is not None]
        return round(statistics.mean(xs), 2) if xs else None
    summary = {"meta": meta}
    for arm in ("deslop", "baseline"):
        a_ai = [r[arm] for r in ai if arm in r]
        a_hu = [r[arm] for r in hu if arm in r]
        if not a_ai:
            continue
        summary[arm] = {
            "ai_score_before": mean(r["before"] for r in ai if arm in r),
            "ai_score_after": mean(x["score"] for x in a_ai),
            "ai_high_left": sum(x["high"] for x in a_ai),
            "human_score_after": mean(x["score"] for x in a_hu),
            "human_similarity": mean(x["similarity"] for x in a_hu),
            "facts_broken": sum(1 for x in a_ai + a_hu if x["facts_hard_fail"]),
            "numbers_added": sum(len(x["added_numbers"]) for x in a_ai + a_hu),
            "numbers_lost": sum(len(x["lost_numbers"]) for x in a_ai + a_hu),
            "markers_ai": sum(x["markers"] for x in a_ai),
            "markers_human": sum(x["markers"] for x in a_hu),
            "tokens_mean": mean(x["tokens"] for x in a_ai + a_hu),
            "seconds_mean": mean(x["seconds"] for x in a_ai + a_hu),
        }
    with open(os.path.join(run_dir, "report.json"), "w") as f:
        json.dump({"summary": summary, "rows": rows}, f, indent=1)
    write_md(run_dir, summary, rows)
    print("\nReport: %s" % os.path.join(run_dir, "report.md"))


def write_md(run_dir, s, rows):
    L = ["# deslop run: %s" % (s.get("meta", {}).get("date", "")), "",
         "Runner: %s, model: %s." % (s.get("meta", {}).get("runner", "?"), s.get("meta", {}).get("model", "?")), "",
         "| | deslop | plain Claude |", "|---|---|---|"]
    keys = [("ai_score_before", "AI samples: score before"), ("ai_score_after", "AI samples: score after"),
            ("ai_high_left", "AI samples: high hits left"), ("human_score_after", "Human samples: score after"),
            ("human_similarity", "Human samples: similarity to original"), ("facts_broken", "Rewrites that broke a number, URL or code"),
            ("numbers_added", "Numbers invented"), ("numbers_lost", "Numbers lost"),
            ("markers_ai", "[NEEDS SPECIFIC] markers, AI samples"), ("markers_human", "[NEEDS SPECIFIC] markers, human samples"),
            ("tokens_mean", "Tokens per run (mean)"), ("seconds_mean", "Seconds per run (mean)")]
    for k, label in keys:
        L.append("| %s | %s | %s |" % (label, s.get("deslop", {}).get(k, "-"), s.get("baseline", {}).get(k, "-")))
    L += ["", "| Sample | Context | Before | deslop | plain | Similarity (deslop) | Markers | Pass 2 similarity |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        d, b, d2 = r.get("deslop", {}), r.get("baseline", {}), r.get("deslop2", {})
        L.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (r["fixture"], r["context"], r["before"], d.get("score", "-"),
                 b.get("score", "-"), d.get("similarity", "-"), d.get("markers", "-"), d2.get("similarity", "-")))
    vp = os.path.join(run_dir, "blind", "verdicts.json")
    if os.path.exists(vp):
        v = json.load(open(vp))
        sm, mn = v["summary"], v["means"]
        L += ["", "## Blind judge (AI samples, both orders)", "",
              "Wins that held in both orders: deslop %d, plain Claude %d, split or tie %d." % (sm["deslop"], sm["plain"], sm["split_or_tie"]),
              "", "| Mean score (1-10) | deslop | plain Claude |", "|---|---|---|"]
        for k in ("human", "specific", "faithful"):
            L.append("| %s | %s | %s |" % (k, mn["deslop_" + k], mn["plain_" + k]))
    with open(os.path.join(run_dir, "report.md"), "w") as f:
        f.write("\n".join(L) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", help="run folder from run_live.py (default: newest in tests/runs)")
    ap.add_argument("--no-runs", action="store_true")
    a = ap.parse_args()
    print("== linter and fact checker")
    unit_tests()
    print("\n== fixtures")
    before = fixture_lint_tests()
    if not a.no_runs:
        run_dir = a.runs
        if not run_dir:
            dirs = sorted(d for d in glob.glob(os.path.join(HERE, "runs", "*")) if os.path.isdir(d))
            run_dir = dirs[-1] if dirs else None
        if run_dir:
            print("\n== saved run: %s" % run_dir)
            run_tests(run_dir, before)
    failed = [n for n, ok, _ in RESULTS if not ok]
    print("\n%d passed, %d failed" % (len(RESULTS) - len(failed), len(failed)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
