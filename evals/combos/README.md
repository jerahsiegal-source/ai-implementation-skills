# Combo tests

Do the skills make the work better, alone and together? Each test runs the same real task several ways:

- **none:** plain Claude or Codex, no skills.
- **one skill:** the skill that fits the task best.
- **stacked:** 3 or 4 skills used together, the way you would in real work.

A skill or a stack is worth keeping only if it clearly beats **none** in blind judging. If a stack doesn't beat its best single skill, the extra skills aren't adding anything for that kind of task.

## The tasks

`scenarios.json` holds each task, its arms and what the judge should focus on. Files the task needs live in `fixtures/`.

| Task | Arms |
|---|---|
| cafe-report | none, chart, visualize, chart+visualize+design |
| signup-build | none, design, design+flow-ux |
| client-tracker | none, design, intent-brief+explore+design+work-loop |

## How to run

1. **Get the prompt for each arm.** Every run uses the same words:
   `node evals/combos/prompt.mjs <task> <arm> --skills <skills folder> --out runs/<task>/<arm>`
   (in folder names, `+` becomes `_`).
2. **Run each prompt** in a fresh Claude Code or Codex session, for example `claude -p "$(node evals/combos/prompt.mjs ...)"`. The none arm must not have the skills installed.
3. **Score with the checkers:** `node evals/combos/score.mjs runs` writes `runs/scores.json` (FAIL and WARN counts for every page).
4. **Judge blind:** `node evals/combos/blind.mjs runs` copies each task's arms into shuffled folders A, B, C and writes `judge-prompt.md`. Give that prompt to a fresh session that has no skills and has not seen the runs. Keep `blind/key.json` away from the judge.
5. **Read the results:** unblind with `key.json` and put the scores on one page, made with `/visualize`.

Run it again when a new model comes out, in both Claude Code and Codex. One run per arm is noisy: when two arms are close, run both again before deciding.
