---
name: skill-review
description: Check how the skills are doing and decide what to keep, fix or cut. Reads private usage history and lab test results, builds the Skill Health page, and turns misses into fixes. Use only when the user types /skill-review or $skill-review.
disable-model-invocation: true
---

# Skill Review

The goal is the user's north star: **the right output the first time, more often than not.** This review checks two signals and acts on them:

- **Real use** (private): how often each skill was right first try, how many fix rounds it took, how often it's used.
- **Lab** (in the repo, `evals/history/`): does the skill still beat plain Claude in blind judging, pass the checkers, and at what token cost.

Run it monthly, after a new model comes out, or whenever a skill feels off. Aim for 15 minutes.

## 1. Gather

From this skill's folder:

```
node scripts/scan.mjs          # reads ~/.claude/projects and ~/.codex/sessions -> ~/.ai-skills/personal/usage-auto.jsonl
node scripts/dashboard.mjs     # -> ~/.ai-skills/personal/skill-health.html and skill-health.json
```

Open the page for the user. Use `skill-health.json` for the rest of this review. Everything personal stays in `~/.ai-skills/personal/`. Never copy usage rows, notes, project names or transcripts into the repo.

## 2. Read the misses

For each skill marked **Fix**, open its misses (notes, follow-up asks, and the session file if needed). Find the pattern in one line, for example "charts pick bars for time series" or "pages too wordy". A guessed miss (no `/rate`) can be a false alarm; check the follow-up text before acting on it.

## 3. Decide, using the rules

Thresholds are in [rules.json](rules.json). Defaults:

| Signal | Verdict | Action |
|---|---|---|
| Wins blind vs plain Claude, right first try 50%+ | Keep | Nothing |
| Right first try under 50% over the last 10 uses | Fix | Steps 4 to 6 |
| No blind win on the latest model | Watch | Re-run that skill's lab test once |
| No blind win on two runs in a row | Cut | The model caught up. Propose archiving |
| Not used in 60 days | Cut | Ask the user once |
| Over 2x plain Claude's tokens, no clear win | Trim | Shorten the skill or drop steps, re-test |
| A stack no better than its best single skill | Trim | Say to use the single skill for that kind of task |
| The user's current model has no lab run | Re-test | Run the full lab (step 7) |

Cut and archive only with the user's OK.

## 4. Turn the miss into a test

Add a case to `skills/<name>/evals/evals.json` that reproduces the miss, with one expectation that fails today. Make it generic: no client names, real data, private paths or personal details, because the repo is public. Put any needed files in `evals/fixtures/`. Each new case is a permanent regression test.

## 5. Fix the skill

Change the smallest thing in `SKILL.md` or its references that addresses the pattern. Keep the skill short. Explain why, not only the rule.

## 6. Prove it

Run that skill's evals with and without the change (skill-creator's benchmark in Claude Code, or `evals/combos` for a full task). Keep the change only if the new case passes and nothing else got worse. If it didn't help, revert and note it in the reply.

## 7. Full lab run (new model, or every 3 months)

Run every task in `evals/combos/` (see its README) in Claude Code, and in Codex where possible. Judge twice with independent shuffles (`blind.mjs runs --tag 2`) so a win only counts when it holds in both orders. Then record it:

```
node scripts/record.mjs <runs-dir> --model <model id> --tool claude-code --blind2 <runs-dir>/blind-2
```

This writes `evals/history/<date>-<model>-<tool>.json`. Commit it: lab results hold no personal data.

## Reply

Open the Skill Health page. Then 5 lines or fewer: right-first-try rate and its trend, what you changed and whether the lab confirmed it, and what needs the user (cuts to approve, a lab run to start).

---
Created by Jerah Siegal · https://www.linkedin.com/in/jerah-siegal-ai-tech/ · MIT License
