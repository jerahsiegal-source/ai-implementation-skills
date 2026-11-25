#!/usr/bin/env python3
"""Learn from the user's own edits. Stdlib only.

deslop writes a draft; the user edits it into a final. This script saves the
pair privately and describes what the user changed, so the model can turn the
changes into preferences that later runs follow.

Everything goes to the user's private folder, never into a repo:
  ~/.ai-skills/personal/deslop/         (or $AI_SKILLS_PERSONAL/deslop/)
    history/<stamp>-<context>/          deslop's recent outputs (original.md, draft.md)
    pairs/<stamp>-<context>/            draft.md, final.md, original.md, meta.json
    preferences.md                      learned cleanup rules (written by the model)
    lint-overrides.json                 rules the user doesn't want (lint.py reads it)

Voice is not deslop's job. If the my-voice folder exists
(~/.ai-skills/personal/my-voice/, or $MY_VOICE_HOME), each pair is also written
to my-voice/edits/ in that skill's format, so one learner owns voice.

  python3 learn.py save --original in.md --draft out.md --context report
  python3 learn.py find final.md                    # best matching saved draft
  python3 learn.py add --draft out.md --final final.md [--original in.md] [--context report] [--note "..."]
  python3 learn.py add --final final.md             # finds the draft in history
  python3 learn.py diff draft.md final.md           # analysis only, saves nothing
  python3 learn.py prefs                            # print the preferences file and its path
  python3 learn.py score                            # how close saved drafts were to finals

`save` is a no-op unless the personal folder exists (install.sh / install.ps1
create it), so nothing is written on machines that didn't opt in.
"""
import argparse
import datetime
import difflib
import json
import os
import re
import shutil
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lint  # noqa: E402

MARKER = re.compile(r"\s*\[NEEDS SPECIFIC:[^\]]*\]")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$|^\s*\*\*([^*\n]+)\*\*\s*$", re.M)
BULLET = re.compile(r"^\s*([-*+]|\d+[.)])\s+", re.M)
HISTORY_KEEP = 50

PREFS_TEMPLATE = """# deslop preferences

Learned from your own edits by `/deslop learn`. Private: this file never goes in a repo.
These are cleanup rules: what to cut, titles, layout, sentence shape, markers.
Voice and word choice belong to your voice skill (my-voice), not here.
A rule applies once it is `confirmed` or seen 2+ times. Edit or delete any line.

## Rules

## Candidates (seen once)
"""


def personal_root():
    base = os.environ.get("AI_SKILLS_PERSONAL") or os.path.join(os.path.expanduser("~"), ".ai-skills", "personal")
    return base


def voice_edits_dir():
    home = os.environ.get("MY_VOICE_HOME") or os.path.join(personal_root(), "my-voice")
    return os.path.join(home, "edits") if os.path.isdir(home) else None


def writing_root(create=False):
    w = os.path.join(personal_root(), "deslop")
    if create:
        os.makedirs(w, exist_ok=True)
    return w


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(p, text):
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)


def stamp():
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")


def similarity(a, b):
    a, b = MARKER.sub("", a).split(), MARKER.sub("", b).split()
    return round(difflib.SequenceMatcher(None, a, b, autojunk=False).ratio(), 3)


# -- analysis ---------------------------------------------------------------

def sentences(text):
    body = HEADING.sub("", MARKER.sub("", text))
    body = BULLET.sub("", body)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])|\n\s*\n", body)
    return [p.strip() for p in parts if len(p.split()) >= 2]


def shape(text):
    s = sentences(text)
    lens = [len(x.split()) for x in s]
    heads = [(m.group(1) or m.group(2)).strip() for m in HEADING.finditer(text)]
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    return {
        "words": len(MARKER.sub("", text).split()),
        "sentences": len(s),
        "mean_sentence_words": round(statistics.mean(lens), 1) if lens else 0,
        "sentence_length_spread": round(statistics.pstdev(lens), 1) if len(lens) > 1 else 0,
        "paragraphs": len(paras),
        "bullets": len(BULLET.findall(text)),
        "headings": heads,
        "markers": len(re.findall(r"\[NEEDS SPECIFIC:", text)),
        "em_dashes": text.count("—"),
        "exclamations": text.count("!"),
        "contractions": len(re.findall(r"\b\w+'(?:s|t|re|ve|ll|d|m)\b", text, re.I)),
    }


def phrase_changes(draft, final, limit=40):
    """Word runs the user cut, added or replaced."""
    a, b = MARKER.sub("", draft).split(), MARKER.sub("", final).split()
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    cut, added, replaced = [], [], []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        x, y = " ".join(a[i1:i2]), " ".join(b[j1:j2])
        if op == "delete":
            cut.append(x)
        elif op == "insert":
            added.append(y)
        elif op == "replace":
            replaced.append({"from": x, "to": y})
    trim = lambda xs: xs[:limit]  # noqa: E731
    return {"cut": trim(cut), "added": trim(added), "replaced": trim(replaced)}


def rule_changes(draft, final, context):
    ld, lf = lint.lint(draft, context), lint.lint(final, context)

    def ids(r):
        out = {}
        for h in r["hits"]:
            out[h["id"]] = out.get(h["id"], 0) + 1
        return out

    d, f = ids(ld), ids(lf)
    return {
        "score_draft": ld["score"],
        "score_final": lf["score"],
        # rules the user's final still breaks: maybe the user doesn't mind them
        "kept_by_user": {k: v for k, v in f.items() if v >= d.get(k, 0) and v > 0},
        # rules the user fixed that deslop missed
        "fixed_by_user": {k: d[k] - f.get(k, 0) for k in d if d[k] > f.get(k, 0)},
    }


def analyse(draft, final, context="general"):
    sd, sf = shape(draft), shape(final)
    markers_left = re.findall(r"\[NEEDS SPECIFIC:[^\]]*\]", final)
    return {
        "context": context,
        "similarity": similarity(draft, final),
        "shape": {"draft": sd, "final": sf},
        "phrases": phrase_changes(draft, final),
        "rules": rule_changes(draft, final, context),
        "markers_answered": sd["markers"] - len(markers_left),
        "markers_left": markers_left,
    }


# -- store ------------------------------------------------------------------

def save_history(original, draft, context):
    if not os.path.isdir(personal_root()):
        return None
    h = os.path.join(writing_root(create=True), "history")
    d = os.path.join(h, "%s-%s" % (stamp(), context))
    os.makedirs(d, exist_ok=True)
    write(os.path.join(d, "original.md"), original)
    write(os.path.join(d, "draft.md"), draft)
    old = sorted(os.listdir(h))
    for x in old[:-HISTORY_KEEP]:
        shutil.rmtree(os.path.join(h, x), ignore_errors=True)
    return d


def find_draft(final):
    h = os.path.join(writing_root(), "history")
    best = (0.0, None)
    if os.path.isdir(h):
        for x in os.listdir(h):
            p = os.path.join(h, x, "draft.md")
            if os.path.exists(p):
                s = similarity(read(p), final)
                if s > best[0]:
                    best = (s, os.path.join(h, x))
    return best


def add_pair(draft, final, original=None, context="general", note=""):
    d = os.path.join(writing_root(create=True), "pairs", "%s-%s" % (stamp(), context))
    os.makedirs(d, exist_ok=True)
    write(os.path.join(d, "draft.md"), draft)
    write(os.path.join(d, "final.md"), final)
    if original:
        write(os.path.join(d, "original.md"), original)
    a = analyse(draft, final, context)
    write(os.path.join(d, "meta.json"), json.dumps({"context": context, "note": note, "similarity": a["similarity"],
                                                    "date": datetime.date.today().isoformat()}, indent=1))
    prefs = os.path.join(writing_root(), "preferences.md")
    if not os.path.exists(prefs):
        write(prefs, PREFS_TEMPLATE)
    ve = voice_edits_dir()
    if ve:  # hand the same pair to my-voice's learner, in its format
        os.makedirs(ve, exist_ok=True)
        now = datetime.datetime.now()
        vp = os.path.join(ve, "%s-%s.md" % (now.strftime("%Y-%m-%d-%H%M%S"), context))
        write(vp, "# Edit | %s | %s\n\n## Before\n\n%s\n\n## After\n\n%s\n\n## User's words\n\n%s\n" % (
            context, now.date().isoformat(), draft.strip(), final.strip(), (note or "(edited a deslop draft)").strip()))
        a["voice_edit"] = vp
    a["pair"] = d
    a["preferences"] = prefs
    return a


def score_pairs():
    p = os.path.join(writing_root(), "pairs")
    rows = []
    if os.path.isdir(p):
        for x in sorted(os.listdir(p)):
            d = os.path.join(p, x)
            if os.path.exists(os.path.join(d, "final.md")):
                rows.append({"pair": x, "similarity": similarity(read(os.path.join(d, "draft.md")), read(os.path.join(d, "final.md")))})
    mean = round(statistics.mean(r["similarity"] for r in rows), 3) if rows else None
    return {"pairs": rows, "mean_similarity": mean}


def to_text(a):
    sd, sf = a["shape"]["draft"], a["shape"]["final"]
    L = ["Similarity draft -> final: %.0f%%" % (a["similarity"] * 100), "", "Shape (draft -> final):"]
    for k in ("words", "sentences", "mean_sentence_words", "sentence_length_spread", "paragraphs", "bullets",
              "markers", "em_dashes", "exclamations", "contractions"):
        if sd[k] != sf[k]:
            L.append("  %-24s %s -> %s" % (k, sd[k], sf[k]))
    if sd["headings"] != sf["headings"]:
        L.append("  headings: %s -> %s" % (sd["headings"], sf["headings"]))
    ph = a["phrases"]
    for k in ("cut", "added"):
        if ph[k]:
            L += ["", "%s:" % k.capitalize()] + ["  - %s" % x for x in ph[k]]
    if ph["replaced"]:
        L += ["", "Replaced:"] + ["  - %s  =>  %s" % (r["from"], r["to"]) for r in ph["replaced"]]
    r = a["rules"]
    L += ["", "Lint score: %s -> %s" % (r["score_draft"], r["score_final"])]
    if r["fixed_by_user"]:
        L.append("  You fixed (deslop missed): %s" % r["fixed_by_user"])
    if r["kept_by_user"]:
        L.append("  You kept (maybe fine for you): %s" % r["kept_by_user"])
    L.append("Markers answered: %d, left: %d" % (a["markers_answered"], len(a["markers_left"])))
    if a.get("pair"):
        L += ["", "Saved pair: %s" % a["pair"], "Preferences: %s" % a["preferences"]]
    if a.get("voice_edit"):
        L.append("Also sent to my-voice: %s" % a["voice_edit"])
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("save")
    s.add_argument("--original", required=True)
    s.add_argument("--draft", required=True)
    s.add_argument("--context", default="general")
    f = sub.add_parser("find")
    f.add_argument("final")
    ad = sub.add_parser("add")
    ad.add_argument("--draft")
    ad.add_argument("--final", required=True)
    ad.add_argument("--original")
    ad.add_argument("--context", default="")
    ad.add_argument("--note", default="")
    ad.add_argument("--text", action="store_true")
    df = sub.add_parser("diff")
    df.add_argument("draft")
    df.add_argument("final")
    df.add_argument("--context", default="general")
    df.add_argument("--text", action="store_true")
    sub.add_parser("prefs")
    sub.add_parser("score")
    a = ap.parse_args()

    if a.cmd == "save":
        d = save_history(read(a.original), read(a.draft), a.context)
        print(d or "personal folder not set up; nothing saved")
    elif a.cmd == "find":
        s, d = find_draft(read(a.final))
        print(json.dumps({"match": d, "similarity": s}))
    elif a.cmd == "add":
        final = read(a.final)
        original, ctx = read(a.original) if a.original else None, a.context
        if a.draft:
            draft = read(a.draft)
        else:
            s, d = find_draft(final)
            if not d or s < 0.3:
                print("No saved deslop draft matches this final (best %.0f%%). Pass --draft." % (s * 100), file=sys.stderr)
                return 2
            draft = read(os.path.join(d, "draft.md"))
            if not original and os.path.exists(os.path.join(d, "original.md")):
                original = read(os.path.join(d, "original.md"))
            ctx = ctx or os.path.basename(d).split("-")[-1]
        res = add_pair(draft, final, original, ctx or "general", a.note)
        print(to_text(res) if a.text else json.dumps(res, indent=1))
    elif a.cmd == "diff":
        res = analyse(read(a.draft), read(a.final), a.context)
        print(to_text(res) if a.text else json.dumps(res, indent=1))
    elif a.cmd == "prefs":
        p = os.path.join(writing_root(), "preferences.md")
        print(p)
        if os.path.exists(p):
            print(read(p))
    elif a.cmd == "score":
        print(json.dumps(score_pairs(), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
