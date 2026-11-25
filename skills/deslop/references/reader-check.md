# Reader check

The linter and `facts.py` prove that tells are gone and facts are kept. They can't tell you whether the text now reads like a person wrote it. This check does. It runs after step 5 whenever the text was AI-written: in `mode=rewrite`, or when the first lint score was below 85.

## Who reads

Use a fresh reader if you can: a subagent (Claude Code's Agent tool, or a new agent in Codex) given only this brief, the original and the rewrite. It hasn't seen your reasoning, so it reads the way the real reader will. If you can't start one, do it yourself: read the rewrite top to bottom as if you had never seen it.

## The brief

Read the ORIGINAL, then the REWRITE. Answer each question with PASS, or with the exact sentences that fail and a one-line fix for each.

1. **Person or model?** Would a reader guess a model wrote this? Quote any sentence that still sounds generated: a template opener, a tidy wrap-up, a pitch, a sentence that says how important something is.
2. **Variety.** Do sentences vary in length and shape? Quote any run of three or more with the same length or the same opening.
3. **Fluff.** Does every sentence carry a fact, a decision, a reason or a request? Quote any that doesn't.
4. **Titles and layout.** Are titles a few plain words, with no "Title: subtitle" and no subtitle line? Would a person have laid it out this way, or is it a template (every bullet a `Label: value`, headings a short text doesn't need, sections that repeat each other)?
5. **Same detail.** Is every fact and useful detail from the original still there, at the same precision? Was anything added that the original didn't say? A `[NEEDS SPECIFIC: ...]` marker is not an addition.
6. **Better?** Is the rewrite clearly better to read than the original? If not, say what holds it back in one line.

End with `VERDICT: PASS` or `VERDICT: FIX` and the list of fixes.

## After the verdict

On FIX, apply only the listed fixes, then re-run the linter and `facts.py` (step 5) and ask again. Stop after two rounds (three in `mode=rewrite`), even if it still says FIX, and list what is left under CHANGES as "Reader notes not fixed". Never invent a detail to satisfy the reader; use a marker.
