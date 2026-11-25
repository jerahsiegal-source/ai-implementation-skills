#!/usr/bin/env python3
"""deslop linter: finds patterns that make text read as AI-generated.

Deterministic, stdlib only. Rules live in rules.json next to this file.

  python3 lint.py draft.md --context report
  cat draft.txt | python3 lint.py --context email --text
  python3 lint.py README.md --context docs --allow-em-dash --max-high 0

Output (JSON, default):
  {context, score, words, counts_by_category, counts_by_severity, hits: [
     {id, name, category, severity, line, col, match, suggestion}]}

Exit code: 1 when high-severity hits exceed --max-high (default 0) or the
score is below --fail-under; 2 on usage errors; otherwise 0.
"""
import argparse
import json
import math
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTEXTS = ["general", "resume", "report", "email", "social", "docs", "web"]
SEV_ORDER = {"low": 1, "medium": 2, "high": 3}
CATEGORY_BY_PREFIX = {"W": "words", "P": "phrases", "S": "structures", "F": "formatting"}

EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF"
    "☀-➿⭐⭕✅❌✨‼⁉\U0001F1E6-\U0001F1FF]"
)
BULLET_RE = re.compile(r"^(\s*)(?:[-*+•▪●]|\d+[.)])\s+(.*)$")
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$")
SMALL_WORDS = {"a", "an", "the", "and", "or", "but", "for", "nor", "on", "at", "to", "by",
               "of", "in", "with", "as", "vs", "via", "from", "into", "is", "are"}
STOCK_VERBS = re.compile(
    r"^(spearhead|leverag|orchestrat|hon|streamlin|utiliz|synergiz|champion|foster|empower|"
    r"facilitat|operationaliz|drove|driv|deliver|optimiz|enhanc|implement|develop|manag|led|"
    r"collaborat|execut|establish|launch|transform|pioneer|revamp|elevat|accelerat)", re.I)


# ---------------------------------------------------------------- helpers

def mask_text(text):
    """Blank out spans the linter must not judge, keeping offsets intact.

    Masks fenced code, indented code, inline code, URLs, markdown link
    targets, HTML tags, blockquotes, quoted speech and [NEEDS SPECIFIC]
    markers. Returns (masked_text, code_mask) where code_mask marks code only.
    """
    chars = list(text)

    def blank(a, b):
        for i in range(a, b):
            if chars[i] != "\n":
                chars[i] = " "

    # fenced code blocks
    for m in re.finditer(r"(?ms)^\s{0,3}(```|~~~).*?^\s{0,3}\1[^\n]*$", text):
        blank(m.start(), m.end())
    # unclosed fence: mask to end
    fences = [m for m in re.finditer(r"(?m)^\s{0,3}(```|~~~)", "".join(chars))]
    if fences:
        blank(fences[0].start(), len(chars))
    # indented code (4+ spaces after a blank line), not list continuations
    lines = "".join(chars).split("\n")
    pos, prev_blank, in_code = 0, True, False
    for ln in lines:
        is_code = (ln.startswith("    ") or ln.startswith("\t")) and ln.strip() and \
            (prev_blank or in_code) and not BULLET_RE.match(ln)
        if is_code:
            blank(pos, pos + len(ln))
        in_code = bool(is_code) or (in_code and not ln.strip())
        prev_blank = not ln.strip()
        pos += len(ln) + 1
    cur = "".join(chars)
    patterns = [
        r"`[^`\n]+`",                                  # inline code
        r"\]\([^)\s]*\)",                              # link targets
        r"<https?://[^>]+>",
        r"\bhttps?://[^\s)>\]]+",                      # URLs
        r"\bwww\.[^\s)>\]]+",
        r"<[^>\n]{1,200}>",                            # HTML tags
        r"(?m)^\s{0,3}>.*$",                           # blockquotes
        r"\[NEEDS SPECIFIC:[^\]]*\]",                  # our own markers
        r"\{%.*?%\}|\{\{.*?\}\}",                      # template tags
    ]
    for p in patterns:
        for m in re.finditer(p, cur):
            blank(m.start(), m.end())
        cur = "".join(chars)
    # quoted material (straight or curly double quotes, one paragraph max)
    for m in re.finditer(r"“[^”\n]{1,400}”|\"[^\"\n]{1,400}\"", cur):
        blank(m.start() + 1, m.end() - 1)
    return "".join(chars)


def code_spans(text):
    """Text of fenced and inline code, for fact checks."""
    blocks = re.findall(r"(?ms)^\s{0,3}(?:```|~~~).*?^\s{0,3}(?:```|~~~)[^\n]*$", text)
    inline = re.findall(r"`[^`\n]+`", re.sub(r"(?ms)^\s{0,3}(?:```|~~~).*?^\s{0,3}(?:```|~~~)[^\n]*$", "", text))
    return blocks, inline


def line_col(text, offset):
    line = text.count("\n", 0, offset) + 1
    col = offset - (text.rfind("\n", 0, offset) + 1) + 1
    return line, col


def words_in(s):
    return re.findall(r"[A-Za-z0-9][A-Za-z0-9'’-]*", s)


def paragraphs(masked):
    """Yield (start_offset, block_text) for blank-line separated blocks."""
    for m in re.finditer(r"(?s)(?:[^\n]|\n(?!\s*\n))+", masked):
        if m.group().strip():
            yield m.start(), m.group()


def is_prose_block(block):
    lines = [l for l in block.split("\n") if l.strip()]
    if not lines:
        return False
    for l in lines:
        if BULLET_RE.match(l) or HEADING_RE.match(l) or l.strip().startswith("|"):
            return False
    return True


SENT_SPLIT = re.compile(r"(?<=[.!?])[\"”')\]]*\s+(?=[\"“(\[]?[A-Z0-9])")


def sentences(block_start, block):
    """Split a prose block into (offset, sentence) pairs."""
    out = []
    pos = 0
    flat = block
    for part in SENT_SPLIT.split(flat):
        idx = flat.find(part, pos)
        if idx < 0:
            idx = pos
        if part.strip():
            out.append((block_start + idx, part))
        pos = idx + len(part)
    return out


# ---------------------------------------------------------------- linter

class Linter:
    def __init__(self, rules, context="general", allow_em_dash=False):
        if context not in rules["contexts"]:
            raise ValueError("unknown context %r (use one of %s)" % (context, ", ".join(rules["contexts"])))
        self.rules = rules
        self.context = context
        self.allow_em_dash = allow_em_dash
        ctx = rules["contexts"][context]
        self.overrides = ctx.get("overrides", {})
        self.enabled = set(ctx.get("enable", []))
        self.hits = []

    # severity after context override; None means off
    def sev(self, rule_id, base):
        if rule_id in self.rules["checks"] and self.rules["checks"][rule_id].get("default") == "off" \
                and rule_id not in self.enabled:
            return None
        s = self.overrides.get(rule_id, base)
        return None if s == "off" else s

    def add(self, rule_id, name, severity, start, end, suggestion, raw=None):
        if severity is None:
            return
        line, col = line_col(self.text, start)
        self.hits.append({
            "id": rule_id,
            "name": name,
            "category": CATEGORY_BY_PREFIX[rule_id[0]],
            "severity": severity,
            "line": line,
            "col": col,
            "match": (raw if raw is not None else self.text[start:end]).strip()[:120],
            "suggestion": suggestion,
            "_start": start,
            "_end": end,
        })

    def run(self, text):
        self.text = text
        self.masked = mask_text(text)
        self.word_list = list(re.finditer(r"[A-Za-z0-9][A-Za-z0-9'’-]*", self.masked))
        self.n_words = len(self.word_list)
        self.regex_rules()
        self.cluster_words()
        self.check_triplets()
        self.check_rhythm()
        self.check_bullets()
        self.check_paragraph_closers()
        self.check_one_liners()
        self.check_first_person()
        self.check_hedges()
        self.check_em_dash()
        self.check_quotes()
        self.check_emoji()
        self.check_bold()
        self.check_headings()
        self.check_long_titles()
        self.check_label_bullets()
        self.check_markdown_plain()
        self.check_hashtags()
        self.check_exclaims()
        self.dedupe()
        return self.report()

    # -- regex based rules
    def regex_rules(self):
        groups = [self.rules["word_rules"], self.rules["phrase_rules"], self.rules["structure_rules"]]
        for group in groups:
            for r in group:
                sev = self.sev(r["id"], r["severity"])
                if sev is None:
                    continue
                pats = []
                for t in r.get("terms", []):
                    pats.append(r"(?<![\w-])(?:%s)(?![\w-])" % t)
                pats.extend(r.get("patterns", []))
                for p in pats:
                    for m in re.finditer(p, self.masked, re.I):
                        g = r.get("group")
                        s, e = (m.start(g), m.end(g)) if g and m.group(g) else (m.start(), m.end())
                        if r.get("unless_number_in_sentence") and self._number_near(s):
                            continue
                        self.add(r["id"], r["name"], sev, s, e, r["suggestion"])

    def _number_near(self, offset):
        a = max(self.masked.rfind(".", 0, offset), self.masked.rfind("\n", 0, offset))
        b_candidates = [i for i in (self.masked.find(".", offset), self.masked.find("\n", offset)) if i >= 0]
        b = min(b_candidates) if b_candidates else len(self.masked)
        return bool(re.search(r"\d", self.text[a + 1:b]))

    def cluster_words(self):
        cfg = self.rules["cluster"]
        idx = [h for h in self.hits if h["category"] in cfg["categories"]]
        if not idx:
            return
        starts = [w.start() for w in self.word_list]

        def word_index(off):
            lo, hi = 0, len(starts)
            while lo < hi:
                mid = (lo + hi) // 2
                if starts[mid] <= off:
                    lo = mid + 1
                else:
                    hi = mid
            return lo
        pos = [word_index(h["_start"]) for h in idx]
        for i, h in enumerate(idx):
            near = sum(1 for p in pos if abs(p - pos[i]) <= cfg["window_words"] // 2)
            target = None
            if near >= cfg["high_at"]:
                target = "high"
            elif near >= cfg["medium_at"]:
                target = "medium"
            if target and SEV_ORDER[target] > SEV_ORDER[h["severity"]]:
                h["severity"] = target
                h["name"] += " (cluster)"

    # -- S-01 triplets
    def check_triplets(self):
        cfg = self.rules["checks"]["S-01"]
        sev = self.sev("S-01", cfg["severity"])
        if sev is None:
            return
        item = r"[a-z][\w'\u2019-]*(?: [a-z][\w'\u2019-]*){0,2}"
        pat = re.compile(r"(?<!, )(?<![\w'])(%s), (%s),? (?:and|or) (%s)\b" % (item, item, item))
        found = []
        for line_m in re.finditer(r"[^\n]+", self.masked):
            line = line_m.group()
            if HEADING_RE.match(line):
                continue
            for m in pat.finditer(line):
                items = [m.group(1), m.group(2), m.group(3)]
                lens = [len(x.split()) for x in items]
                # lists of names, numbers or long uneven clauses are real lists, not a habit
                if max(lens) - min(lens) > 1:
                    continue
                found.append((line_m.start() + m.start(), line_m.start() + m.end()))
        if not found:
            return
        rate = len(found) / max(self.n_words, 1) * 500
        s = cfg["escalated_severity"] if rate >= cfg["escalate_per_500_words"] else sev
        if SEV_ORDER.get(s, 0) < SEV_ORDER[sev]:
            s = sev
        for a, b in found:
            self.add("S-01", cfg["name"], s, a, b, cfg["suggestion"])

    # -- S-04 sentence rhythm
    def check_rhythm(self):
        cfg = self.rules["checks"]["S-04"]
        sev = self.sev("S-04", cfg["severity"])
        if sev is None:
            return
        sents = []
        for start, block in paragraphs(self.masked):
            if is_prose_block(block):
                sents.extend(sentences(start, block))
        lens = [len(words_in(s)) for _, s in sents]
        lens_pairs = [(o, s, n) for (o, s), n in zip(sents, lens) if n >= 3]
        if len(lens_pairs) >= cfg["min_sentences"]:
            ls = [n for _, _, n in lens_pairs]
            mean = statistics.mean(ls)
            cv = statistics.pstdev(ls) / mean if mean else 0
            if cv < cfg["cv_below"]:
                s = "high" if cv < cfg["high_cv_below"] and sev != "low" else sev
                o = lens_pairs[0][0]
                self.add("S-04", cfg["name"], s, o, o + 1, cfg["suggestion"],
                         raw="sentence length varies too little (CV %.2f over %d sentences, mean %.0f words)" % (cv, len(ls), mean))
                return
        # runs of near-equal length sentences
        run = 1
        for i in range(1, len(lens_pairs)):
            if abs(lens_pairs[i][2] - lens_pairs[i - 1][2]) <= cfg["run_tolerance_words"]:
                run += 1
                if run == cfg["run_length"]:
                    o = lens_pairs[i - run + 1][0]
                    self.add("S-04", cfg["name"], "low" if sev != "off" else None, o, o + 1, cfg["suggestion"],
                             raw="%d sentences in a row of about %d words" % (run, lens_pairs[i][2]))
            else:
                run = 1

    # -- S-05 same-shape bullets (and resume stock verb runs)
    def bullet_runs(self):
        runs, cur = [], []
        for m in re.finditer(r"[^\n]*", self.masked):
            line = m.group()
            b = BULLET_RE.match(line)
            if b and b.group(2).strip():
                cur.append((m.start() + b.start(2), b.group(2)))
            elif line.strip() == "" and cur:
                continue
            else:
                if cur:
                    runs.append(cur)
                cur = []
        if cur:
            runs.append(cur)
        return runs

    def check_bullets(self):
        cfg = self.rules["checks"]["S-05"]
        sev = self.sev("S-05", cfg["severity"])
        if sev is None:
            return
        for run in self.bullet_runs():
            if len(run) < cfg["min_run"]:
                continue
            firsts = []
            for off, content in run:
                w = words_in(re.sub(r"^[*_]+", "", content))
                w = [x for x in w if x.lower() not in ("a", "an", "the")] or w
                firsts.append(w[0].lower() if w else "")
            # same first word
            i = 0
            while i < len(run):
                j = i
                while j + 1 < len(run) and firsts[j + 1] == firsts[i] and firsts[i]:
                    j += 1
                if j - i + 1 >= cfg["min_run"]:
                    self.add("S-05", cfg["name"], sev, run[i][0], run[j][0] + len(run[j][1]), cfg["suggestion"],
                             raw="%d bullets in a row start with '%s'" % (j - i + 1, firsts[i]))
                i = j + 1
            # stock verb / past-tense power verb class
            cls = [bool(STOCK_VERBS.match(f)) or (f.endswith("ed") and len(f) > 4) for f in firsts]
            i = 0
            while i < len(run):
                if not cls[i]:
                    i += 1
                    continue
                j = i
                while j + 1 < len(run) and cls[j + 1]:
                    j += 1
                n = j - i + 1
                stock = sum(1 for k in range(i, j + 1) if STOCK_VERBS.match(firsts[k]))
                need = cfg["min_run"] if self.context == "resume" else max(cfg["min_run"], 4)
                if n >= need and (stock >= cfg["min_run"] or n == len(run)) and len(set(firsts[i:j + 1])) > 1:
                    s = sev
                    if self.context == "resume" and stock >= cfg["min_run"]:
                        s = "high"
                    self.add("S-05", cfg["name"], s, run[i][0], run[j][0] + len(run[j][1]), cfg["suggestion"],
                             raw="%d bullets in a row open with a stock action verb (%s)" % (n, ", ".join(firsts[i:j + 1])))
                i = j + 1
            # 'resulting in' tails repeated across a list
            tails = [k for k, (_, c) in enumerate(run) if re.search(r",? (resulting in|leading to|which (resulted|led) (in|to))\b", c, re.I)]
            if len(tails) >= 2:
                for h in self.hits:
                    if h["id"] == "S-06" and any(run[k][0] <= h["_start"] <= run[k][0] + len(run[k][1]) for k in tails):
                        if SEV_ORDER[h["severity"]] < SEV_ORDER["medium"]:
                            h["severity"] = "medium"

    # -- S-08 summary sentence at paragraph end
    def check_paragraph_closers(self):
        cfg = self.rules["checks"]["S-08"]
        sev = self.sev("S-08", cfg["severity"])
        if sev is None:
            return
        pat = re.compile(r"^\s*(?:%s)\b" % "|".join(cfg["starts"]), re.I)
        for start, block in paragraphs(self.masked):
            if not is_prose_block(block):
                continue
            ss = sentences(start, block)
            if len(ss) < 2:
                continue
            off, last = ss[-1]
            if pat.match(last):
                self.add("S-08", cfg["name"], sev, off, off + len(last), cfg["suggestion"])

    # -- S-13 one-line paragraph drama
    def check_one_liners(self):
        cfg = self.rules["checks"]["S-13"]
        sev = self.sev("S-13", cfg["severity"])
        if sev is None:
            return
        blocks = [(s, b) for s, b in paragraphs(self.masked)]
        run = []
        for s, b in blocks + [(None, None)]:
            short = b is not None and is_prose_block(b) and "\n" not in b.strip() and \
                len(words_in(b)) <= cfg["max_words"] and len(sentences(0, b)) <= 1
            if short:
                run.append((s, b))
                continue
            if len(run) >= cfg["min_run"]:
                self.add("S-13", cfg["name"], sev, run[0][0], run[-1][0] + len(run[-1][1]), cfg["suggestion"],
                         raw="%d one-line paragraphs in a row" % len(run))
            run = []

    # -- S-14 first person in resume
    def check_first_person(self):
        cfg = self.rules["checks"]["S-14"]
        sev = self.sev("S-14", cfg["severity"])
        if sev is None:
            return
        for m in re.finditer(r"(?<![\w'])(?:I|I'm|I've|my|me|myself)(?![\w'])", self.masked):
            if m.group() == "I" and re.match(r"\s*[.)]", self.masked[m.end():m.end() + 2]):
                continue
            self.add("S-14", cfg["name"], sev, m.start(), m.end(), cfg["suggestion"])

    # -- P-05 hedge stacks
    def check_hedges(self):
        cfg = self.rules["checks"]["P-05"]
        sev = self.sev("P-05", cfg["severity"])
        if sev is None:
            return
        pat = re.compile(r"\b(?:%s)\b" % "|".join(re.escape(h) for h in sorted(cfg["hedges"], key=len, reverse=True)), re.I)
        for line_m in re.finditer(r"[^\n]+", self.masked):
            for sent_off, sent in sentences(line_m.start(), line_m.group()):
                ws = list(re.finditer(r"\S+", sent))
                hs = [(m.start(), m.end()) for m in pat.finditer(sent)]
                if len(hs) < cfg["min_hedges"]:
                    continue
                widx = [sum(1 for w in ws if w.start() < h[0]) for h in hs]
                for i in range(len(hs) - 1):
                    if widx[i + 1] - widx[i] <= cfg["window_words"]:
                        self.add("P-05", cfg["name"], sev, sent_off + hs[i][0], sent_off + hs[i + 1][1], cfg["suggestion"])
                        break

    # -- F-01 em dashes
    def check_em_dash(self):
        if self.allow_em_dash:
            return
        cfg = self.rules["checks"]["F-01"]
        sev = self.sev("F-01", cfg["severity"])
        if sev is None:
            return
        found = list(re.finditer(r"—|(?<=[A-Za-z,]) – (?=[A-Za-z])|(?<=[A-Za-z]) -- (?=[A-Za-z])|&mdash;", self.masked))
        if not found:
            return
        rate = len(found) / max(self.n_words, 1) * 300
        s = cfg["escalated_severity"] if rate > cfg["escalate_per_300_words"] else sev
        for m in found:
            self.add("F-01", cfg["name"], s, m.start(), m.end(), cfg["suggestion"],
                     raw=self.text[max(0, m.start() - 15):m.end() + 15].replace("\n", " "))

    # -- F-02 mixed quotes
    def check_quotes(self):
        cfg = self.rules["checks"]["F-02"]
        sev = self.sev("F-02", cfg["severity"])
        if sev is None:
            return
        prose = mask_text(self.text.replace('"', "\u0001")).replace("\u0001", '"')
        curly_d = len(re.findall("[“”]", self.text))
        straight_d = len(re.findall(r'(?<![=\w])"|"(?![\w=:])', prose))
        curly_s = len(re.findall("[‘’]", self.text))
        straight_s = len(re.findall(r"(?<=\w)'(?=\w)", prose))
        if (curly_d and straight_d) or (curly_s and straight_s):
            m = re.search("[“”‘’]", self.text)
            self.add("F-02", cfg["name"], sev, m.start(), m.end(), cfg["suggestion"],
                     raw="curly %d/%d, straight %d/%d (double/single)" % (curly_d, curly_s, straight_d, straight_s))

    # -- F-03 emoji
    def check_emoji(self):
        cfg = self.rules["checks"]["F-03"]
        sev = self.sev("F-03", cfg["severity"])
        if sev is None:
            return
        for m in EMOJI_RE.finditer(self.masked):
            line_start = self.masked.rfind("\n", 0, m.start()) + 1
            prefix = self.masked[line_start:m.start()]
            as_bullet = not prefix.strip() or re.fullmatch(r"\s*(?:#{1,6}|[-*+])\s*", prefix)
            s = cfg["bullet_severity"] if as_bullet else sev
            if self.context == "social" and not as_bullet:
                s = self.overrides.get("F-03", sev) if s != "off" else None
            self.add("F-03", cfg["name"], s, m.start(), m.end(), cfg["suggestion"])

    # -- F-04 bold mid-sentence
    def check_bold(self):
        cfg = self.rules["checks"]["F-04"]
        sev = self.sev("F-04", cfg["severity"])
        if sev is None:
            return
        found = []
        for m in re.finditer(r"(\*\*|__)(?=\S)(.+?)(?<=\S)\1", self.masked):
            line_start = self.masked.rfind("\n", 0, m.start()) + 1
            prefix = self.masked[line_start:m.start()]
            if re.fullmatch(r"\s*(?:[-*+]|\d+[.)])?\s*", prefix):
                continue  # bold at line start is a label, F-07 handles it
            found.append(m)
        s = cfg["escalated_severity"] if len(found) >= cfg["escalate_at"] else sev
        for m in found:
            self.add("F-04", cfg["name"], s, m.start(), m.end(), cfg["suggestion"])

    # -- F-05 Title Case headings, F-06 too many headings
    def check_headings(self):
        heads = []
        for m in re.finditer(r"[^\n]+", self.masked):
            h = HEADING_RE.match(m.group())
            if h:
                heads.append((m.start(), h.group(2)))
        cfg5 = self.rules["checks"]["F-05"]
        sev5 = self.sev("F-05", cfg5["severity"])
        if sev5 and len(heads) >= cfg5["min_headings"]:
            def title_case(t):
                ws = [w for w in re.findall(r"[A-Za-z][\w'-]*", t)]
                big = [w for w in ws[1:] if w.lower() not in SMALL_WORDS]
                return len(ws) >= 3 and len(big) >= 2 and all(w[0].isupper() for w in big) \
                    and not all(w.isupper() for w in big)
            tc = [(o, t) for o, t in heads if title_case(t)]
            if len(tc) >= cfg5["min_headings"] and len(tc) >= len(heads) / 2:
                for o, t in tc:
                    self.add("F-05", cfg5["name"], sev5, o, o + len(t) + 3, cfg5["suggestion"], raw=t)
        cfg6 = self.rules["checks"]["F-06"]
        sev6 = self.sev("F-06", cfg6["severity"])
        if sev6 and heads and self.n_words <= cfg6["max_words"] and len(heads) >= 3 \
                and self.n_words / len(heads) < cfg6["words_per_heading_below"]:
            o = heads[0][0]
            self.add("F-06", cfg6["name"], sev6, o, o + 1, cfg6["suggestion"],
                     raw="%d headings in %d words" % (len(heads), self.n_words))

    # -- F-11 long titles and subtitles
    def check_long_titles(self):
        cfg = self.rules["checks"]["F-11"]
        sev = self.sev("F-11", cfg["severity"])
        if sev is None:
            return
        lines = list(re.finditer(r"[^\n]+", self.masked))
        for i, m in enumerate(lines):
            line = m.group()
            h = HEADING_RE.match(line)
            b = re.match(r"^\s*\*\*([^*\n]+?)\*\*\s*$", line)
            t = (h.group(2) if h else b.group(1) if b else "").strip()
            if not t or t.endswith("?"):  # FAQ questions are fine
                continue
            n = len(re.findall(r"[A-Za-z0-9][\w'-]*", t))
            sub = re.search(r"[A-Za-z]: [A-Za-z]|[A-Za-z] (?:\u2014|\u2013|--) [A-Za-z]", t)
            # an italic line right under a title is a subtitle
            nxt = lines[i + 1].group().strip() if i + 1 < len(lines) and lines[i + 1].start() == m.end() + 1 else ""
            sub_line = h and h.group(1) == "#" and re.match(r"^[*_][^*_\n]{12,}[*_]$", nxt)
            if n > cfg["max_words"] or sub or sub_line:
                why = "%d words" % n if n > cfg["max_words"] else "title with a subtitle"
                self.add("F-11", cfg["name"], sev, m.start(), m.end(), cfg["suggestion"], raw="%s (%s)" % (t, why))

    # -- F-07 label: explanation bullets
    def check_label_bullets(self):
        cfg = self.rules["checks"]["F-07"]
        sev = self.sev("F-07", cfg["severity"])
        if sev is None:
            return
        lab = re.compile(r"^\s*(?:\*\*|__)?[A-Z][^:\n]{1,40}?(?:\*\*|__)?:(?:\*\*|__)?\s+\S")
        for run in self.bullet_runs():
            flags = [bool(lab.match(c)) for _, c in run]
            i = 0
            while i < len(run):
                if not flags[i]:
                    i += 1
                    continue
                j = i
                while j + 1 < len(run) and flags[j + 1]:
                    j += 1
                if j - i + 1 >= cfg["min_run"]:
                    self.add("F-07", cfg["name"], sev, run[i][0], run[j][0] + len(run[j][1]), cfg["suggestion"],
                             raw="%d 'Label: text' bullets in a row" % (j - i + 1))
                i = j + 1

    # -- F-08 markdown in plain-text contexts
    def check_markdown_plain(self):
        cfg = self.rules["checks"]["F-08"]
        sev = self.sev("F-08", cfg["severity"])
        if sev is None:
            return
        for m in re.finditer(r"(?m)^\s{0,3}#{1,6}\s|\*\*[^*\n]+\*\*|__[^_\n]+__|^\s*[-*]\s+\[[ x]\]|^\s*\|.*\|\s*$", self.masked):
            self.add("F-08", cfg["name"], sev, m.start(), m.end(), cfg["suggestion"])

    # -- F-09 hashtag wall
    def check_hashtags(self):
        cfg = self.rules["checks"]["F-09"]
        sev = self.sev("F-09", cfg["severity"])
        if sev is None:
            return
        tags = list(re.finditer(r"(?<![\w#&])#[A-Za-z]\w+", self.masked))
        if len(tags) >= cfg["min_hashtags"]:
            self.add("F-09", cfg["name"], sev, tags[0].start(), tags[-1].end(), cfg["suggestion"],
                     raw="%d hashtags" % len(tags))

    # -- F-10 exclamation marks
    def check_exclaims(self):
        cfg = self.rules["checks"]["F-10"]
        sev = self.sev("F-10", cfg["severity"])
        if sev is None:
            return
        found = [m for m in re.finditer(r"(?<=\w)!(?!\w)", self.masked)]
        s = cfg["escalated_severity"] if len(found) >= cfg["escalate_at"] else sev
        for m in found:
            self.add("F-10", cfg["name"], s, max(0, m.start() - 20), m.end(), cfg["suggestion"])

    # -- keep the strongest hit when two rules match the same span
    def dedupe(self):
        self.hits.sort(key=lambda h: (h["_start"], -SEV_ORDER[h["severity"]]))
        kept = []
        for h in self.hits:
            dup = False
            for k in kept[-6:]:
                if k["id"][0] in "WP" and h["id"][0] in "WP" and not (h["_end"] <= k["_start"] or h["_start"] >= k["_end"]):
                    dup = True
                    break
            if not dup:
                kept.append(h)
        self.hits = kept

    def report(self):
        sc = self.rules["scoring"]
        penalty = sum(sc["weights"][h["severity"]] for h in self.hits)
        per_k = penalty / max(self.n_words, sc["min_words"]) * 1000
        score = round(100 * math.exp(-sc["decay"] * per_k))
        cats, sevs = {}, {"high": 0, "medium": 0, "low": 0}
        for h in self.hits:
            cats[h["category"]] = cats.get(h["category"], 0) + 1
            sevs[h["severity"]] += 1
        hits = [{k: v for k, v in h.items() if not k.startswith("_")} for h in self.hits]
        return {
            "context": self.context,
            "score": score,
            "words": self.n_words,
            "counts_by_category": cats,
            "counts_by_severity": sevs,
            "hits": hits,
        }


def load_rules(path=None):
    with open(path or os.path.join(HERE, "rules.json"), encoding="utf-8") as f:
        return json.load(f)


def lint(text, context="general", allow_em_dash=False, rules=None):
    return Linter(rules or load_rules(), context, allow_em_dash).run(text)


def to_text(res):
    out = ["SCORE %d/100  (%s, %d words)  high %d  medium %d  low %d" % (
        res["score"], res["context"], res["words"], res["counts_by_severity"]["high"],
        res["counts_by_severity"]["medium"], res["counts_by_severity"]["low"])]
    for h in res["hits"]:
        out.append("%4d:%-3d %-6s %-5s %s  \"%s\"  -> %s" % (
            h["line"], h["col"], h["severity"].upper(), h["id"], h["name"], h["match"], h["suggestion"]))
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Find AI-writing patterns in text. Reads a file or stdin.")
    ap.add_argument("file", nargs="?", help="file to check (default: stdin)")
    ap.add_argument("--context", default="general", choices=CONTEXTS)
    ap.add_argument("--allow-em-dash", action="store_true", help="don't flag em dashes")
    fmt = ap.add_mutually_exclusive_group()
    fmt.add_argument("--json", action="store_true", help="JSON output (default)")
    fmt.add_argument("--text", action="store_true", help="readable output")
    ap.add_argument("--max-high", type=int, default=0, help="exit 1 if high hits exceed this (default 0)")
    ap.add_argument("--fail-under", type=int, default=0, help="exit 1 if the score is below this")
    ap.add_argument("--rules", help="use another rules.json")
    ap.add_argument("--list-rules", action="store_true", help="print rule ids and names, then exit")
    a = ap.parse_args(argv)
    rules = load_rules(a.rules)
    if a.list_rules:
        for grp in ("word_rules", "phrase_rules", "structure_rules"):
            for r in rules[grp]:
                print("%-5s %-7s %s" % (r["id"], r["severity"], r["name"]))
        for k, v in rules["checks"].items():
            print("%-5s %-7s %s%s" % (k, v["severity"], v["name"], " (only in some contexts)" if v.get("default") == "off" else ""))
        return 0
    if a.file:
        with open(a.file, encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()
    res = lint(text, a.context, a.allow_em_dash, rules)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(to_text(res) if a.text else json.dumps(res, indent=2, ensure_ascii=False))
    bad = res["counts_by_severity"]["high"] > a.max_high or res["score"] < a.fail_under
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
