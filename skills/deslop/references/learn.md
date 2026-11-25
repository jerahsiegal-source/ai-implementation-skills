# Learn from the user's edits

deslop gets better for one person by comparing what it wrote with what that person finally sent. Everything learned stays in their private folder, `~/.ai-skills/personal/deslop/`, and never goes into a repo.

## When the user hands back a final

They may paste the final, give a file, or give both the draft and the final. Save the final to a temp file outside the project, then:

```
python3 scripts/learn.py add --final final.md --note "<anything they said about why>" --text
```

If they also gave the draft, add `--draft draft.md`. Without it the script finds the matching deslop output in `history/`. If nothing matches, ask them for the draft deslop gave them (once), or for the original, and run deslop on the original first.

## Turn the diff into rules

Read the script's report: what they cut, added and replaced, how the shape changed (length, sentence length and spread, headings, bullets, paragraphs), which lint rules they fixed that deslop missed, which they kept, and which markers they answered.

Write rules about **how they edit**, not about this text:

- Good: "Cut reassurance closers ('we'll keep you posted', 'let me know if...') in status reports." "Titles: 2 to 4 words, no 'Status' or 'Update'." "Keep one short summary line before a table."
- Bad: "Remove the sentence about Chargebee." (only true once) or anything that copies their facts, names or private content.

Each rule is one line in `preferences.md` under **Candidates (seen once)**, with a scope and a count: `- [all] [seen 1] Cut reassurance closers.` When a new pair shows the same habit, raise the count and move it to **Rules** at 2.

**Scope:** use `[all]` for habits about how the person writes anything (closers they cut, headings they remove, lists they turn into sentences, title length). Use a context such as `[report]` only when the habit clearly depends on the kind of text, such as a resume's section order. A habit counts as seen again in any context, so one in a report and one in an email make 2. Merge near-duplicates into one line instead of adding a new one. Mark a rule `confirmed` if the user says so. If a pair contradicts a rule, say so and lower or remove it.

Lint rules the user keeps on purpose (they leave em dashes in, or keep a list of three) go in `lint-overrides.json` instead, only after two pairs or the user's OK: `{"all": {"F-01": "off"}, "report": {"S-01": "low"}}`. lint.py reads it on its own.

Voice is not deslop's job: word choice, tone, jokes and phrasing they add go to their voice skill. If `~/.ai-skills/personal/my-voice/` exists, `learn.py` already copied the pair to `my-voice/edits/` for it.

## Tell the user

Show only what changed, in a few lines:

```
LEARNED from your report edit (pair 3)
  New rule:     [report] Cut reassurance closers. (seen 2, now applies)
  Candidate:    [report] Titles 2 to 4 words. (seen 1)
  Lint:         em dashes now allowed (you kept them in 3 of 3 finals)
  Your edits vs deslop: 91% the same (was 84% on your first pair)
```

The last line comes from `python3 scripts/learn.py score`: the mean similarity between deslop's drafts and the user's finals. It should rise as deslop learns.
