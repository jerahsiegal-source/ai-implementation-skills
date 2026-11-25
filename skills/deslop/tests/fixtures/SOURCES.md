# Fixture sources

File names are `<id>-<context>-<topic>.md`. The context is the second part, and the tests pass it to the linter.

## ai/ (model-written; should be flagged and fixed)

Raw output from plain Claude in Claude Code (`claude -p`, no skills installed), generated on 2026-11-25 with the Haiku and Sonnet aliases of that date. Prompts were the kind a person would type, such as "Write a cover letter for a UX designer applying to a senior designer role at Calder Studio." Company and person names are made up.

- `a01` to `a13`, `a19`: plain prompts. These show what current models write by default, which is cleaner than 2023-era output.
- `a14` to `a18` (`-classic`): the prompt asked for "the way a 2023 ChatGPT answer typically sounded (eager, generic, polished)". They stand in for the older, heavier style that hiring managers and readers complain about.
- `a06`, `a07`, `a16`, `a19` carry many numbers, dates and names for the fact-preservation checks. `a10` is a README with code blocks for the code-safety check.

## human/ (written by people before 2023; should pass mostly untouched)

All public domain or MIT. Excerpts were trimmed to 150 to 450 words. Markup was simplified (template tags and images removed, hard-wrapped lines joined); the wording is unchanged.

| File | Source | License |
|---|---|---|
| h01, h02, h03, h04, h05, h06, h09, h11, h12, h13 | 18F blog posts, 2014 to 2016 ([18F/18f.gsa.gov](https://github.com/18F/18f.gsa.gov), `content/posts/`) | US government work, public domain; CC0 worldwide |
| h07, h08 | VA letters from plainlanguage.gov examples ([GSA/plainlanguage.gov](https://github.com/GSA/plainlanguage.gov)); h08 is the "before" version | US government work, public domain |
| h10 | Express 4.17.1 README ([expressjs/express](https://github.com/expressjs/express/blob/4.17.1/Readme.md), 2019) | MIT |
| h14 | JSON Resume sample resume ([jsonresume/resume-schema](https://github.com/jsonresume/resume-schema), v1.0.0), laid out as plain text; the person is fictional | MIT |

The human set deliberately includes things a naive checker would flag: em dashes, lists of three, "robust", bold labels, "deeply value", "transform federal digital services". The point is to prove that deslop leaves real human writing alone.
