# deslop

Removes the patterns that make writing read as AI-generated, and flags vague claims that need a real detail. Facts, names, numbers, code and quotes stay exactly as they were. Text that is already clean comes back unchanged.

Works in Claude Code and Codex. Use it on its own, or as the last pass of another writing skill.

```
/deslop resume
<paste text, or give a file path>
```

```
SCORE: 1 → 88   (context: resume)
NEEDS YOUR INPUT (2):
  - Line 4: [NEEDS SPECIFIC: which lead capture methods?]
  - Line 6: [NEEDS SPECIFIC: open rate from what to what?]

CLEAN TEXT:
...

CHANGES:
  - Cut 3 cliches (results-driven, proven track record, passionate about)
  - Removed 2 stock verbs (leveraging, partnered closely)
  - Turned 2 vague results into questions for you
FACTS: all numbers, names, URLs and code kept.
```

## Why

Readers don't reject text because AI touched it. They reject it because it is vague.

- In Resume Genius's 2026 survey of hiring managers, 80% said they can often tell a resume is AI-written, and 76% said AI-written resumes make it harder to see what the candidate actually did. A Resume Now survey found 62% reject AI resumes that lack personalization.
- Originality.ai found LinkedIn posts flagged as likely AI got about 45% less engagement, and LinkedIn now has a "Seems like AI slop" feedback option.
- AI detectors mostly measure predictability, and they are unreliable: a Stanford study (Liang et al., 2023) found seven detectors flagged 61% of essays by non-native English speakers as AI-written. So deslop doesn't try to beat a detector. It fixes specificity and rhythm, which is what readers notice.
- Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) warns that the surface signs are symptoms. Text with the tells scrubbed out and nothing specific inside is still bad. That's why deslop has a content pass and the `[NEEDS SPECIFIC]` marker, not just a word list.
- Practitioners combine a deterministic linter (finds things reliably, can't rewrite) with a model rewrite (rewrites well, misses things), then check the result again. deslop does exactly that.

## How it works

1. **Lint.** `scripts/lint.py` finds 42 kinds of pattern (stock words, chatbot leftovers, contrast frames, rule-of-three habits, flat sentence rhythm, same-shape bullets, em dashes, emoji, label bullets, markdown in email, unfilled placeholders and more) and scores the text 0 to 100. It skips code, URLs and quotes.
2. **Content pass.** The model reads for what no regex can see: claims with no anchor, sentences that could be in anyone's resume, inflated importance, repetition.
3. **Rewrite, minimum change.** Only flagged sentences change. Where a detail is missing it writes `[NEEDS SPECIFIC: question?]` instead of inventing one.
4. **Check.** Lint again, and run `scripts/facts.py` to confirm no number, name, URL, quote or code changed. At most two passes.

Contexts change what counts as a problem: `resume`, `report`, `email` (also cover letters), `social`, `docs`, `web`, `general`. Action verbs are fine in a resume; emoji are not fine in an email. See [contexts](references/contexts.md).

## Install

From the repo root, `./install.sh` (Mac/Linux) or `.\install.ps1` (Windows) links every skill, including this one, into `~/.claude/skills` and `~/.agents/skills`. Needs Python 3 for the scripts; no packages to install.

## Use

| You want | Type |
|---|---|
| Clean a draft | `/deslop` and paste it (Codex: `$deslop`) |
| Set the context | `/deslop email`, `/deslop web` ... |
| Keep em dashes | `/deslop keep em dashes` |
| Only see the problems | `/deslop mode=check` |
| Clean a file in place | `/deslop docs README.md` |
| Lint without the model | `python3 scripts/lint.py draft.md --context report --text` |
| Fail CI on slop | `python3 scripts/lint.py README.md --context docs --max-high 0` (exit 1 on any high hit) |

It also starts on its own when you ask to "humanize", "de-slop" or "make this sound less AI-written".

**From another skill.** Call `deslop context=<type> mode=embedded` with the text. It returns only `CLEAN TEXT:` and `NEEDS YOUR INPUT (n):`, so a voice skill can write first and hand the draft to deslop as the last step. deslop has no voice of its own and contains nothing personal.

**Tuning.** Every word list, phrase pattern, severity and context rule is in [`scripts/rules.json`](scripts/rules.json). Run `python3 scripts/lint.py --list-rules` to see them. Change the file, then run the tests.

## Tests

```
python3 tests/run_tests.py            # linter, fact checker, fixtures, newest saved run
python3 tests/run_live.py --jobs 6     # re-run the skill and plain Claude on every fixture
python3 tests/run_live.py --runner codex
```

`tests/fixtures/ai/` holds 19 model-written samples across all seven contexts. `tests/fixtures/human/` holds 14 human samples written before 2023 (public domain and MIT, see [SOURCES](tests/fixtures/SOURCES.md)). `run_live.py` runs each one through deslop, through deslop a second time, and through plain Claude with the same request, then `run_tests.py` checks:

- AI samples: score rises, no high-severity hits left, no fact lost.
- Human samples: at least 85% of words unchanged, at most one `[NEEDS SPECIFIC]` marker.
- Code blocks byte-for-byte unchanged.
- A second pass changes less than 5%.
- deslop vs plain Claude: scores, facts lost or invented, edits to human text, tokens and time.

Results of each run are saved in `tests/runs/<date>-<runner>-<model>/report.md`. Run it again when a new model comes out; if plain Claude catches up, the skill needs changing or cutting.

## Limits

- The linter is English-only.
- It can't tell whether a number is true. It only checks that the rewrite didn't change it.
- Current models write fewer surface tells than 2023 models. On their output, most of the value is the content pass and the markers, which depend on the model doing its part.
- Scores are a guide, not a verdict. A human text can score 70 because the author likes em dashes and lists of three.

## Credits and licenses

deslop's rules are written in our own words. No text was copied from the projects below; their ideas shaped the structure.

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), WikiProject AI Cleanup (CC BY-SA 4.0). The main catalog of tells and the "symptoms, not the problem" warning. Paraphrased, not quoted.
- [blader/humanizer](https://github.com/blader/humanizer) (MIT, Siqi Chen). Pattern catalog from the Wikipedia guide, and the list of things that are not reliable AI signs, which became deslop's protect-list.
- [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) (MIT, Hardik Pandya). The SKILL.md plus `references/` layout, and the core rules: cut filler, break contrasts, reduce triples, vary rhythm, trust the reader.
- [rbaddam/humanizer](https://github.com/rbaddam/humanizer) (Apache 2.0). Tone per context, and never touching API names, product names or versions.
- [timolabs-ai/claude-humanize-skill](https://github.com/timolabs-ai/claude-humanize-skill) (MIT, TIMO Labs). Rule priority (facts first, style last) and checks on bullets, paragraphs and section narration.
- [realrossmanngroup/no_ai_slop_writing_rules](https://github.com/realrossmanngroup/no_ai_slop_writing_rules) (no license file found). Reviewed for ideas only.
- [Slop Guard](https://eric-tramel.github.io/blog/2026-02-18-slop-guard/) by Eric Tramel. Scoring by penalty per 1,000 words with exponential decay, and the sentence-length variance check.
- [unsloppify](https://petems.github.io/unsloppify/) by Peter Souter (MIT). Rules in an editable data file, JSON output, and a non-zero exit code for CI.
- Human test samples: 18F and plainlanguage.gov (US government, public domain), Express (MIT), JSON Resume (MIT).

MIT License, like the rest of this repo.
