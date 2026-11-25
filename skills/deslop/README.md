# deslop

Removes the patterns that make writing read as AI-generated, and flags vague claims that need a real detail. Facts, names, numbers, code and quotes stay exactly as they were. Text that is already clean comes back unchanged.

Works in Claude Code and Codex. Use it on its own, or as the last pass of another writing skill.

```
/deslop resume
<paste text, or give a file path>
```

```
SCORE: 1 → 100   (context: resume)
NEEDS YOUR INPUT (2):
  - Line 5: [NEEDS SPECIFIC: which lead capture channels?]
  - Line 8: [NEEDS SPECIFIC: by how much?]

CLEAN TEXT:
Marketing Manager who runs email marketing in HubSpot, from audience
segmentation to performance reporting. Grew Acme Retail's newsletter
list from 8,000 to 21,000 subscribers.
...

CHANGES:
  - Cut 4 cliches (results-driven, proven track record, passionate about, eager to bring)
  - Removed 3 vague impact phrases (driving growth, data-driven insights, deliver measurable results)
  - Cut "partnered closely with cross-functional teams" to "worked with the sales, design and e-commerce teams"
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
| Rewrite text you know is AI-written, more freely | `/deslop mode=rewrite` |
| Teach it from the version you actually sent | `/deslop learn` and paste your final |
| Clean a file in place | `/deslop docs README.md` |
| Lint without the model | `python3 scripts/lint.py draft.md --context report --text` |
| Fail CI on slop | `python3 scripts/lint.py README.md --context docs --max-high 0` (exit 1 on any high hit) |

It also starts on its own when you ask to "humanize", "de-slop" or "make this sound less AI-written".

**Teach it your edits.** After you edit a deslop draft, give it back with `/deslop learn`. deslop compares its draft with your final, writes your habits as one-line rules in `~/.ai-skills/personal/deslop/preferences.md`, and follows them from then on (a rule applies once it shows up twice, or when you confirm it). Lint rules you keep breaking on purpose go in `lint-overrides.json` next to it. All of it stays on your computer and never goes in the repo. Voice and word choice are left to a voice skill: if `~/.ai-skills/personal/my-voice/` exists, each pair is copied to its `edits/` folder too. `python3 scripts/learn.py score` shows how close deslop's drafts are getting to your finals.

**From another skill.** Call `deslop context=<type> mode=embedded` with the text. It returns only `CLEAN TEXT:` and `NEEDS YOUR INPUT (n):`, so a voice skill can write first and hand the draft to deslop as the last step. deslop has no voice of its own and contains nothing personal.

**Tuning.** Every word list, phrase pattern, severity and context rule is in [`scripts/rules.json`](scripts/rules.json). Run `python3 scripts/lint.py --list-rules` to see them. Change the file, then run the tests.

## Tests

```
python3 tests/run_tests.py            # linter, fact checker, fixtures, newest saved run
python3 tests/run_live.py --jobs 6     # re-run the skill and plain Claude on every fixture
python3 tests/run_live.py --runner codex
python3 tests/judge.py --runs tests/runs/<run>   # blind A/B judge, both orders
```

`tests/fixtures/ai/` holds 19 model-written samples across all seven contexts. `tests/fixtures/human/` holds 14 human samples written before 2023 (public domain and MIT, see [SOURCES](tests/fixtures/SOURCES.md)). `run_live.py` runs each one through deslop, through deslop a second time, and through plain Claude with the same request, then `run_tests.py` checks:

- AI samples: score rises, no high-severity hits left, no fact lost.
- Human samples: at least 85% of words unchanged, at most one `[NEEDS SPECIFIC]` marker.
- Code blocks byte-for-byte unchanged.
- A second pass changes less than 5%.
- deslop vs plain Claude: scores, facts lost or invented, edits to human text, tokens and time.
- A blind judge (a fresh model with no skills) compares deslop and plain Claude on each AI sample in both A/B orders, because the linter alone would be grading its own homework. A win counts only if it holds in both orders.

Results of each run are saved in `tests/runs/<date>-<runner>-<model>/report.md`. Run it again when a new model comes out; if plain Claude catches up, the skill needs changing or cutting.

## Results (2026-11-25, Claude Code, default model)

33 samples, each run through deslop and through plain Claude with the same one-line request. Full table: [tests/runs/2026-11-25-claude-code-opus-5-5-v3/report.md](tests/runs/2026-11-25-claude-code-opus-5-5-v3/report.md).

| | deslop | plain Claude |
|---|---|---|
| AI samples, linter score (before 50) | 80 | 71 |
| High-severity hits left | 0 | 2 |
| Human samples, words kept unchanged | 98% | 54% |
| Rewrites that lost or changed a number, URL or code | 0 of 33 | 5 of 33 |
| Blind judge, wins held in both orders (19 AI samples) | 8 | 9 (2 split) |
| Blind judge, "reads like a person" (1-10) | 6.5 | 8.0 |
| Blind judge, "specific" / "faithful" (1-10) | 7.3 / 8.6 | 6.6 / 7.8 |
| Tokens per run | about 147k | about 41k |

Where it wins: no rewrite lost or changed a number, URL or code; it leaves human writing alone; and it marks missing details instead of making them up. The judge noted plain Claude adding details the original never gave on 8 of 19 samples. Where it doesn't: plain Claude's freer rewrites read more natural; on clean-looking modern model output deslop often changes nothing; and the judge noted deslop dropping a non-numeric point from the original on 5 samples, which `facts.py` can't catch. Earlier runs (v1, v2) are kept next to v3 for comparison.

### Rewrite mode (`mode=rewrite`, with the reader check)

For text you know is AI-written. Same 19 AI samples, judged blind in both orders on reads human, sentence variety, no fluff, specific, and faithful. Full results: [tests/runs/2026-11-25-claude-code-opus-5-5-rewrite/](tests/runs/2026-11-25-claude-code-opus-5-5-rewrite/blind/).

| Version (vs plain Claude) | Wins | Losses | Reads human | Variety | No fluff | Faithful | Cost per text |
|---|---|---|---|---|---|---|---|
| Default deslop | 5 | 8 | 6.5 vs 8.1 | 5.7 vs 7.5 | 7.4 vs 7.6 | 8.6 vs 7.8 | ~$0.15 |
| `mode=rewrite`, no reader check | 11 | 6 | 7.2 vs 8.1 | 6.5 vs 7.5 | 8.1 vs 7.6 | 8.4 vs 7.8 | ~$0.20 |
| `mode=rewrite` + reader check (shipped) | 13 | 4 | 7.7 vs 7.8 | 7.1 vs 7.3 | 8.5 vs 7.3 | 8.5 vs 7.6 | ~$0.41 |
| Driven by the Work Loop skill (6 samples) | 4 | 2 | 7.7 vs 7.8 | 7.0 vs 7.2 | 8.2 vs 7.7 | 8.8 vs 8.3 | ~$0.75 |

The reader check closed most of the gap on how human the text reads, and the judge picked deslop over plain Claude on 13 of 19. Head to head on 6 samples, the shipped version and the Work Loop split 3 to 2 (one tie), so the Work Loop isn't worth twice the cost for a single document. No rewrite lost or changed a real number, URL or code (`facts.py` flags one social post where "Lesson 1–5" labels and three hashtags were dropped).

### Learning from edits (simulated user)

`tests/run_learning.py` gives a scripted editor three fixed habits (no titles on short pieces, no follow-up closers, short lists as sentences), lets it edit 4 deslop drafts, and runs `/deslop learn` on each. deslop found all three habits after 4 edits and wrote them as cross-context rules. One reached "seen twice" on its own; the other two waited for a second sighting or the user's OK. With all three confirmed, habit breaks on 5 new drafts went from 4 to 3, and no facts were lost. The rules it wrote were narrower than the editor's real habits (it learned "lists of about 3 items", so a 5-item list stayed). Learning follows what your edits show, so it gets sharper as you hand back more finals.

## Limits

- The linter is English-only.
- It can't tell whether a number is true. It only checks that the rewrite didn't change it.
- `facts.py` checks numbers, names, URLs, quotes and code. A dropped claim in plain words ("teamwork", "clear communication") isn't caught.
- Current models write fewer surface tells than 2023 models. On their output, the linter often scores 85+ and deslop returns the text almost unchanged, even when it still reads stiff.
- Minimum change is a trade-off: it protects human writing and facts, but a free rewrite reads more natural to a blind judge.
- Costs about 3.5x the tokens of a plain rewrite, mostly from loading the skill and running the scripts.
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
