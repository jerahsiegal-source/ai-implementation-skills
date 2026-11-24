---
name: flow-ux
description: Review a user flow (sign-up, checkout, setup, a form, navigation) by actually walking through it, then rank the problems by severity with a screenshot for each, and fix them on request. Use only when the user types /flow-ux or $flow-ux.
disable-model-invocation: true
---

# Flow UX

Find out whether a real person can finish the task, and where they get stuck. Look rules ask "does it look right?". This skill asks "does it work for a person trying to get something done?".

Two modes:
- **Review** (default): walk the flow, report ranked findings with screenshots. Change nothing.
- **Fix** (when the user says "fix", or inside a work loop): review, fix the findings, then walk the flow again until it passes.

When `/design` pulls this skill in while building, apply only [the rules](references/rules.md). Don't run a full review unasked.

Read [the floor](../design-kit/floor.md) first, plus `DESIGN.md` and `~/.ai-skills/personal/taste.md` if they exist. The user's words win over all of them.

## 1. Frame (state it, don't interview)

In three lines:
- **Who:** the person doing it, and what they know coming in (first-timer, returning, expert).
- **Task:** what they are trying to finish, in their words ("send my first invoice").
- **Done:** the screen or result that means they finished.

If `INTENT.md` exists, take these from it. Ask only if the task is truly unclear. A review with no task is a style critique, not a flow review.

## 2. Walk it for real

- **Drive the real thing.** Open the running app, preview or HTML in a browser (Playwright or the tool's browser) and complete the task as that person would. Reading code alone is not a review. If nothing runs, say so and review screenshots or a design file instead, labelled as such.
- **Record every step:** a screenshot of each screen (save to `./flow-ux/<task>/`), the action taken, and what the person has to read, decide or type.
- **Walk it three ways:** the happy path; a mistake path (wrong input, back button, refresh, empty fields, slow or failed request); and keyboard only. Then repeat the happy path at phone width (about 390px).
- **Count the cost:** steps, decisions, fields, and anything the person must remember from one screen to the next.
- **Run the checker on each distinct screen** that is an HTML page or URL:
  `node ../design-kit/scripts/check-page.mjs <page or url> --out ./flow-ux/<task>/checks`
  Contrast, tiny text, phone overflow and console errors are flow problems too.

## 3. Ask the four questions at every step

This is a cognitive walkthrough. At each step, for this person:

1. **Will they try to do the right thing?** Do they know what this step is for?
2. **Will they see how?** Is the control visible and where they'd look?
3. **Will they know it's the right control?** Does its label match their goal in their words?
4. **Will they know it worked?** Is there clear feedback and an obvious next step?

Any "no" is a finding. Then sweep the whole flow with the [heuristics](references/heuristics.md).

## 4. Rank the findings

Each finding gets:
- **Severity** 0 to 4 (from the [heuristics](references/heuristics.md)): 4 blocks the task, 3 major, 2 minor, 1 cosmetic, 0 not a real problem (drop it).
- **Where:** step number and the screenshot path.
- **What happens:** what the person sees or does, in one sentence. No jargon.
- **Fix:** the smallest change that solves it.
- **Evidence:** the question or heuristic it fails, or the checker line.

Never report a finding you didn't see happen or can't point to on a screenshot. Merge duplicates. Keep the list to what matters: every 4 and 3, the worst 2s, and a count of the rest.

## 5. Report

- If the `visualize` skill is installed, make the report with it: the flow as a **Mission Map** (one box per step, findings pinned to the step they occur on, the worst steps marked At risk), a **Decision Desk** for any fix that needs the user's choice, and the screenshots one click away.
- Otherwise write `./flow-ux/<task>/review.md`: the frame, a one-line verdict ("Can a first-timer finish? Yes, with 2 major snags"), the step table (step, screenshot, cost), then findings by severity.
- Start with the verdict and the count: `0 blockers · 2 major · 5 minor`.

## 6. Fix mode

1. Fix in severity order, 4s first. Smallest change that solves each one; keep every existing feature.
2. After each fix, walk the affected steps again and re-run the checker on the changed screens.
3. When all 4s and 3s are fixed, walk the whole flow once more (happy, mistake, keyboard, phone) and run the [quality check](../design-kit/quality-check.md).
4. Stop when no 4 or 3 remains and the checker exits 0. If a finding survives two fix attempts, stop on it and report why.
5. Show before and after screenshots for each fixed finding.

Inside a work loop, each user-facing Done item that involves a flow passes only when this walk-through shows no severity 4 or 3 left, with the screenshots shown.

## Reply

5 lines or fewer: the verdict, the counts by severity, the top finding, the report path, and the next step ("Say fix to fix the 4s and 3s").
