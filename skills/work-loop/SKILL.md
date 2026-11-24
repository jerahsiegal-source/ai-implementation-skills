---
name: work-loop
description: Take an INTENT.md and work, check, self-review and fix until every done item passes with real evidence, then hand back a branch plus a review handoff package. Use for big features or fundamental changes the user wants handed off and finished in full ("run the work loop", "loop on this intent", "take this to done"). Not for exploratory or taste-driven work such as UI style options.
---

# Work Loop

Finish the whole job described in `INTENT.md`, prove it the way the owner would check it by hand, review it independently, and stop: done, stuck, or at a gate. Never stop at slice 1 of 6, and never spiral.

Works the same in Claude Code and Codex. Best started under the tool's native `/goal` so it keeps going across turns (see this skill's README for the line to paste). Without `/goal`, run the same loop in-session.

## Ground rules

- **The brief is the contract.** Re-read `INTENT.md` at the start of every iteration. Work only toward its Done items. Respect Never and Stop-and-ask absolutely. Everything under "Yours to decide" is yours: decide, log the decision in one line, move on.
- **Evidence or it didn't happen.** An item passes only when its check ran in this session and the output is shown in the conversation (command output, screenshot, file path, numbers). The `/goal` evaluator and the reviewer see only what you show.
- **Check like the owner would.** User-facing items are proven by driving the real app or product: start the flow, finish it, open the result, inspect its content. Unit tests alone never pass a user-facing item.
- **No fake tests.** New tests must fail without the change and pass with it. Never weaken, skip or delete an existing test or check to get green. Never edit item or check text in `done.json`.
- **Smallest change that meets the intent.** Build on existing patterns; no parallel paths, no drive-by refactors. Out-of-scope findings go to the found-not-fixed list.
- **Visual items.** The look is decided before the loop (`DESIGN.md` or `/explore`); never choose between styles inside the loop. Build with the `design` skill's rules and prove each visual item with the design kit's quality check (desktop and phone screenshots shown in the conversation).
- **Branch, small commits.** Work on a branch, never the default branch. One commit per passed item, so any layer can be rolled back alone. Pushing the branch is fine unless the brief says otherwise. Never deploy to production. Never delete data, branches or files others depend on.

## 1. Setup (once)

1. Read `INTENT.md` (path given by the user; default `./INTENT.md`). If there is none, or Outcome/Done/Never are missing, stop and suggest the `intent-brief` skill.
2. Create a state folder next to the brief, `<brief-folder>/loop/`, holding:
   - `done.json`: one entry per Done item, copied word for word:
     `{"id": "D1", "item": "...", "check": "...", "kind": "user-facing|code|judgment|regression", "status": "pending", "attempts": 0, "evidence": ""}`
     Only `status` (`pending|pass|blocked`), `attempts` and `evidence` may change after setup.
   - `progress.md`: an append-only log, plus three running sections: **Decisions** (choice + one-line why), **Found, not fixed**, and **Blocked**.
3. Pick the base branch and create a working branch. Record both in `progress.md`.
4. **Baseline.** Run the project's existing test suite and checks, and record the results (what passes and what already fails). Define the regression check you will run after every item. If the full suite is too slow for every item, record which subset runs per item; the full suite runs at review and at finish.
5. If a check needs something gated (paid API calls, production, owner credentials), plan around it now: fixtures, recorded outputs or a local environment. If there is no way around it, that item will stop at the gate.
6. Print a short setup summary: the items, base and branch, the baseline, and planned gates.

## 2. Build loop (repeat)

Each iteration:

1. Re-read `INTENT.md`, `done.json`, and the tail of `progress.md`.
2. Pick the next `pending` item, respecting dependencies. Work on **one item** only.
3. Make the change. Run the item's check, then the regression check.
4. **Pass** (check met, nothing that was green turned red): set `status: pass`, record evidence, commit `D<n>: <item>`, log it.
   **Fail:** increment `attempts`, log what was tried and learned. After **2 failed attempts** on the same item, set `status: blocked` with the reason, and move on to the next independent item.
5. Print one status line: `D3 pass | 4/7 passing | 1 blocked`.

Stop rules, checked every iteration:

- **Stall:** two iterations in a row with no newly passing item → stop and report.
- **All remaining items blocked** → stop and report.
- **Never** about to be crossed → stop immediately and report; do not do it.
- **Stop-and-ask gate** reached → finish everything else you can, then print a stop report naming the gate and what is waiting on it. A stop report ends the `/goal` run, so the loop doesn't push past the gate.
- Running out of budget or time is not completion. Report it as a stop.

When every item passes, go to review.

## 3. Review (bounded)

1. Run the full test suite and compare it with the baseline.
2. Start a **fresh reviewer**: a new subagent in the same tool, given [the reviewer brief](references/reviewer-brief.md), `INTENT.md`, `done.json`, `progress.md` and the diff against base. The worker never reviews its own work. If the tool cannot start a subagent, say so and leave review to the handoff.
3. For each finding, record in `progress.md`: **fixed** (with evidence), **disagree** (with evidence), or **declined** (a nit, becomes a follow-up). Re-run the affected checks after any fix.
4. Run another round only while a blocker or should-fix is open. At most **3 rounds**; 5 only for security, auth, permissions or data loss. Stop early when only nits remain.
5. A finding still disputed after two exchanges goes to the owner in the handoff, with both sides in 2–3 lines. Do not agree just to end the loop.
6. If review grew the diff beyond the intent, cut it back.

## 4. Finish

1. Fetch the base branch and confirm the branch merges cleanly (rebase or merge, then re-run the full suite). Resolve conflicts by keeping both intents; if that isn't possible, stop and ask.
2. Push the branch. Open a PR only if the brief asks for one.
3. Write `<brief-folder>/loop/handoff.md` containing:
   - **Summary:** what was built, branch, commits.
   - **Done items:** each with its evidence.
   - **Not done:** blocked or gated items, with reasons.
   - **Decisions made:** each with a one-line why.
   - **Found, not fixed:** follow-ups and declined nits.
   - **Disputes for the owner** (if any).
   - **Cross-model review prompt:** ready to paste into the other tool (Claude Code ↔ Codex). It points to the branch, the brief and this file, and asks for review using the reviewer brief.
   - **Staging test checklist:** the user-facing checks for the owner to repeat by hand.
4. If the `visualize` skill is installed, offer to turn `handoff.md` into a visual page.
5. Print the final report in the conversation: items passing with evidence pointers, anything not done, and the path to `handoff.md`.

## Stop report (any early stop)

Print: why it stopped, items passed / blocked / pending, what is needed from the owner, and where state lives. Leave the branch and state files so a fresh session can resume from Setup step 1, reusing the existing `loop/` folder rather than rebuilding it.

## Resuming

If `<brief-folder>/loop/` already exists, do not recreate it. Read `done.json` and `progress.md`, re-run the baseline and regression checks on the current branch, and continue from the next pending item.
