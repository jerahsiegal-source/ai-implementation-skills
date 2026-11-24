# Skill Review

Are the skills still earning their place? Type `/skill-review` once a month, or when a new model comes out.

It builds one page, **Skill Health**, from two signals:

| Signal | Where it comes from | Private? |
|---|---|---|
| **Right first try**, fix rounds, uses | Your local Claude Code and Codex history, plus any [`/rate`](../rate) | Yes, stays on your computer |
| **Blind wins** vs plain Claude, checker passes, token cost | Lab runs of [`evals/combos`](../../evals/combos), saved in [`evals/history`](../../evals/history) | No, in the repo |

Each skill gets a verdict: **Keep**, **Fix**, **Trim**, **Cut** or **Watch** (rules in [rules.json](rules.json)). For a Fix, it turns the misses into a new test case, changes the skill, and keeps the change only if the lab says it's better.

Preview with sample data:

```
node skills/skill-review/scripts/dashboard.mjs --demo
```

## Scripts

| Script | Job |
|---|---|
| `scan.mjs` | Finds skill uses in your session history and guesses right-first-try from your follow-ups |
| `dashboard.mjs` | Builds the Skill Health page and `skill-health.json` |
| `record.mjs` | Saves a finished lab run to `evals/history/` |
| `test.mjs` | Self-test on the fixtures (runs on every push) |

Needs Node 18 or newer. No packages.

---
