#!/usr/bin/env python3
"""Check that a rewrite kept every fact from the original.

Compares numbers, capitalized names, URLs, inline code, code blocks and
quoted text between two files. Anything lost or added is reported.
[NEEDS SPECIFIC: ...] markers in the rewrite are ignored.

  python3 facts.py original.md rewrite.md            # JSON
  python3 facts.py original.md rewrite.md --text

Exit code: 1 if a code block changed or any fact was lost or added, else 0.
Lost names can be fine (a stock phrase in Title Case that was cut), so read
the list before acting on it; lost numbers, URLs and code never are.
"""
import argparse
import json
import re
import sys
from collections import Counter

MARKER = re.compile(r"\[NEEDS SPECIFIC:[^\]]*\]")
FENCE = re.compile(r"(?ms)^\s{0,3}(```|~~~).*?^\s{0,3}\1[^\n]*$")
# Words that start sentences or headings often; not names on their own.
COMMON = set("""a an the and or but if then so this that these those it its we our you your
they their he she his her i my me us in on at to for from by of with as is are was were be
been being have has had do does did not no yes all any each every some most more many much
new first last next one two three four five six seven eight nine ten what why how when where
who which while after before during about over under into out up down off here there also
just only very can could will would should may might must let lets get got make made use
used using our hi hello dear thanks thank sincerely regards best warm cheers please note
summary overview conclusion introduction background results next steps risks key highlights
experience education skills projects volunteer profile about contact features install
installation usage example examples license credits today tomorrow yesterday monday tuesday
wednesday thursday friday saturday sunday q1 q2 q3 q4""".split())


PLACEHOLDER = re.compile(r"\[[^\]\n]{0,40}\b[XN]\b[^\]\n]{0,40}\]")


def strip(text):
    """Drop our markers and template slots like [X,000] or [N] before comparing."""
    t = PLACEHOLDER.sub(" ", MARKER.sub(" ", text))
    # list numbering ("1.", "2)") and "Lesson 3:" labels are layout, not facts
    t = re.sub(r"(?m)^(\s*)\d{1,2}[.)](?=\s)", r"\1", t)
    return re.sub(r"(?i)\b(lesson|step|tip|part|phase)\s+\d{1,2}\s*:", r"\1:", t)


def numbers(text):
    t = FENCE.sub(" ", strip(text))
    nums = re.findall(r"(?<![\w.])[$€£]?\d[\d,]*(?:\.\d+)?(?:%|k|m|x|\+)?(?![\w])", t, re.I)
    return Counter(n.rstrip(",").replace(",", "") for n in nums)


def names(text):
    t = FENCE.sub(" ", strip(text))
    t = re.sub(r"`[^`\n]+`|https?://\S+", " ", t)
    found = Counter()
    for m in re.finditer(r"\b[A-Z][\w&.'’-]*(?:\s+(?:of|and|&|de|for)?\s*[A-Z][\w&.'’-]*)*", t):
        phrase = m.group().strip(" .'’")
        words = phrase.split()
        if len(words) == 1:
            w = words[0]
            if w.lower() in COMMON:
                continue
            before = t[:m.start()].rstrip()
            sentence_start = not before or before[-1] in ".!?:\n#*-|>(\"“" or t[max(0, m.start() - 1)] == "\n"
            # a lone capitalized word at a sentence start is only a name if it
            # also appears mid-sentence somewhere, or has inner caps/digits
            if sentence_start and not re.search(r"[A-Z]|\d", w[1:]):
                if not re.search(r"(?<![.!?]\s)(?<!^)\b%s\b" % re.escape(w), t[m.end():]):
                    continue
        found[phrase] += 1
    return found


def urls(text):
    return Counter(re.findall(r"https?://[^\s)>\]\"']+", strip(text)))


def inline_code(text):
    return Counter(re.findall(r"`[^`\n]+`", FENCE.sub(" ", text)))


def code_blocks(text):
    return [m.group() for m in FENCE.finditer(text)]


def quotes(text):
    t = FENCE.sub(" ", strip(text))
    return Counter(q for q in re.findall(r"“([^”\n]{3,300})”|\"([^\"\n]{3,300})\"", t) for q in q if q)


def diff(a, b):
    lost = sorted((a - b).elements())
    added = sorted((b - a).elements())
    return lost, added


def name_tokens(counter):
    toks = Counter()
    for k, v in counter.items():
        for w in re.findall(r"[A-Z][\w&'’-]*", k):
            if w.lower() not in COMMON:
                toks[w] += v
    return toks


def compare(original, rewrite):
    res = {}
    for key, fn in (("numbers", numbers), ("urls", urls), ("inline_code", inline_code), ("quotes", quotes)):
        # compare as sets: repeating a fact that is already there is not adding one
        a, b = set(fn(original)), set(fn(rewrite))
        lost, added = sorted(a - b), sorted(b - a)
        res[key] = {"lost": lost, "added": added}
    # names: compare at the word level so "Stripe Billing" vs "Stripe" isn't noise
    a, b = names(original), names(rewrite)
    ta, tb = name_tokens(a), name_tokens(b)
    lost = sorted(set(ta) - set(tb))
    added = sorted(set(tb) - set(ta))
    res["names"] = {"lost": lost, "added": added}
    ca, cb = code_blocks(original), code_blocks(rewrite)
    res["code_blocks"] = {"original": len(ca), "rewrite": len(cb), "changed": ca != cb}
    hard = any(res[k]["lost"] or res[k]["added"] for k in ("numbers", "urls", "inline_code")) or res["code_blocks"]["changed"]
    soft = bool(res["names"]["lost"] or res["names"]["added"] or res["quotes"]["lost"] or res["quotes"]["added"])
    res["ok"] = not hard and not soft
    res["hard_fail"] = hard
    res["markers_added"] = len(MARKER.findall(rewrite)) - len(MARKER.findall(original))
    return res


def to_text(r):
    out = ["FACTS " + ("OK" if r["ok"] else ("CHANGED (numbers, URLs or code)" if r["hard_fail"] else "CHECK names/quotes"))]
    for k in ("numbers", "names", "urls", "inline_code", "quotes"):
        if r[k]["lost"]:
            out.append("  lost %-11s %s" % (k, ", ".join(map(str, r[k]["lost"]))))
        if r[k]["added"]:
            out.append("  added %-10s %s" % (k, ", ".join(map(str, r[k]["added"]))))
    if r["code_blocks"]["changed"]:
        out.append("  code blocks changed (%d before, %d after)" % (r["code_blocks"]["original"], r["code_blocks"]["rewrite"]))
    out.append("  [NEEDS SPECIFIC] markers added: %d" % r["markers_added"])
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check a rewrite kept every number, name, URL, quote and code block.")
    ap.add_argument("original")
    ap.add_argument("rewrite")
    ap.add_argument("--text", action="store_true")
    a = ap.parse_args(argv)
    with open(a.original, encoding="utf-8") as f:
        o = f.read()
    with open(a.rewrite, encoding="utf-8") as f:
        w = f.read()
    r = compare(o, w)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(to_text(r) if a.text else json.dumps(r, indent=2, ensure_ascii=False))
    return 1 if r["hard_fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
