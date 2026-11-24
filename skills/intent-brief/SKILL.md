---
name: intent-brief
description: Run a short interview that turns what the user wants into a one-page intent brief (outcome, why, done-when gates, hard limits) an AI can execute against without being told how. Use when the user wants to hand work to an agent or a do-check-repeat loop, says "get out of the AI's way", "define the intent", "what does done look like", or wants a lighter alternative to Grill Me / a full plan.
---

# Intent Brief

Capture **what** and **why**, never **how**. The brief exists so an executing agent (or a do-work/check-work loop) can make its own implementation choices and still land exactly where the user meant, all the way to done.

Over-specifying is the failure this skill prevents. If a detail would not change whether the result is acceptable, it does not belong in the brief.

## Interview

Start from whatever the user has already said. Do not ask for anything you can already infer — state the inference and let them correct it.

Ask in small batches (one to three questions), only about these five things, in roughly this order:

1. **Outcome** — When this is finished, what exists or is true that is not true now? Push for something observable, not an activity ("users can X", not "work on X").
2. **Why** — What is this for? What decision, problem or person does it serve? The why is what lets the agent resolve ambiguity on its own, so get the real reason.
3. **Done** — How would you check it is finished, in full? List *every* part that must be complete (the whole scope, not the first slice). For each, ask: "If you sat down to check this yourself, what would you do?" That answer is the evidence: clicking through the real app, a report with real content, a passing command, a number, your review. Code-level tests alone are not evidence for anything a user sees.
4. **Never** — What must not happen under any circumstances? (Data, money, production, people, scope, things that would be worse than not doing the work.) Hard limits only — not preferences.
5. **Stop and ask** — Which moments genuinely need you? (Spending past a limit, irreversible actions, a choice only you can make.) Everything else is the agent's call.

## Listening: translate, don't transcribe

Many people describe intent through stories, examples and complaints, often by voice dictation, rather than as tidy requirements. That is rich input; the job is to translate it.

- **Examples carry the intent.** When the user explains through a concrete case ("for example, right now I'm fixing scoring…"), pull out the general rule it illustrates and say it back: "So in general: X. The scoring work is one case of that — right?" Keep the example out of the brief unless it is the acceptance test.
- **Complaints become gates.** Grievances ("it finishes slice 1 of 6", "I have to hand it to review myself") are the sharpest source of Done and Never items. Turn each one into a check that would have caught it.
- **Listed steps or stages are states.** When the user lists the steps something goes through (lead, proposal, signed, live), the thing must hold an item at every step. Add a Done item like "can add and track a client at any step", and never require data from a later step to create an item at an earlier one.
- **Lists of distinctions are requirements.** When the user lists tiers or categories ("good vs very good vs great vs niche"), the ability to tell them apart is usually the outcome. Keep the list.
- **Separate hedges from real uncertainty.** "I think", "I guess", "something along those lines" are often filler around a firm view. Treat the statement as intended unless the user also says they don't know or contradicts it later.
- **"I don't know" is a fine answer.** Propose a sensible default, say why, and move on. Record it as the default, not a decision. Never stall the interview on it.
- **Explicit delegation is permission.** When the user says "that's why I'm handing this to you" or "think this through", make the call yourself and show it in the brief for them to correct.
- **One message, several asks.** Long dictated messages often bundle a second task, a research idea and a side question. Answer the side question briefly, note research ideas under Yours to decide, and give a second task its own brief. If it illustrates this one, make it the acceptance test.
- **Later beats earlier.** People refine as they talk. When a later statement corrects an earlier one, use the later one without making a point of it.
- **Read past transcription noise.** Dictation mangles names and words ("Soul" for "Sol"). Infer the obvious meaning; ask only when a misheard term would change the brief.

Rules for the interview:

- Aim for **five to ten questions total**. Stop as soon as all five sections are answerable.
- Challenge vagueness only where it would let an agent stop early or go somewhere wrong ("better", "clean", "works" → better how, measured by what?).
- When the user starts describing implementation (which library, which file, which steps), ask *why* that matters. If it is a real constraint, keep it as one line under Never or Must. If it is a preference, drop it or mark it as a preference the agent may override.
- Do not draft solutions, plans or task lists. That is the executing agent's job.

## Output: INTENT.md

Write the brief to `INTENT.md` in the active project's working folder (or the location the user names). Keep it to one page. Use the user's own words wherever possible.

```markdown
# Intent: <short name>

## Outcome
<one or two sentences: what is true when this is done>

## Why
<the real reason; what it serves; what a good tradeoff looks like>

## Who uses it (only for things people click through)
- <who> wants to <task in their words>; done when <the screen or result they reach>

## Done when (all must pass)
- [ ] <scope item 1> — evidence: <how it is checked>
- [ ] <scope item 2> — evidence: <...>
- [ ] ...
Partial completion is not done. If any item cannot be met, stop and report which and why.

## Never
- <hard limit>

## Stop and ask before
- <owner gate>

## Yours to decide
Everything not listed above: approach, structure, tools, order, naming. Prefer what best serves the Why.
```

Then read it back to the user in two or three lines and ask one question: "Is this what you mean?" Revise on correction. Do not start the work.

## Clarity rating

After the brief is confirmed, give the user a short rating of how clearly they conveyed their intent, so both they and this skill get better over time. Keep it to a few lines:

- One score per section (Outcome, Why, Done, Never, Stop and ask): **clear**, **inferred** (you had to fill it in from examples or context), or **missing** (a default was used).
- What they did well, in one line, named concretely ("the slice 1 of 6 complaint gave the sharpest gate").
- One tip for next time, aimed at the weakest section ("when you give an example, say which part should generalize").
- One thing the skill should do differently for them, if any.

Rate how well the intent came across, not grammar, length or polish. Dictated, rambling input that carries clear intent rates well.

If the agent has persistent memory, save any durable pattern about how this person describes work (for example, "leads with examples; grievances define gates") so the next interview starts from it. Do not save the rating itself.

## Writing good gates

A gate is a check the loop runs to decide whether to keep going. Good gates make "done" impossible to fake and impossible to stop short of.

- **Cover the whole scope.** Enumerate every slice, page, segment, file or case that must be done. "All 6 tiers render" beats "tiers render". If the scope is a set, name the set or how to count it.
- **Name the evidence.** Each item says how it is verified: command and expected result, artifact path, metric threshold, or "owner review" when only judgment works.
- **Prefer objective over judgment.** Use owner review only where no check exists, and say what the owner will look at.
- **Check outcomes, not effort.** "Report shows a score for every segment" not "scoring code updated".
- **Include one end-to-end check** that proves the pieces work together, not only separately.
- **Include a no-regressions check** for changes to existing systems: what already worked still works.
- **Things people click through** (apps, sign-ups, forms, dashboards): ask who uses it and the 1 to 3 tasks they must finish, and write them under **Who uses it**. Gate each task as a flow: "A first-time <who> can <task> with no blocker or major problem", evidence: the `flow-ux` walk-through with screenshots.
- **Visual work:** settle the look first (`/explore`, or an existing `DESIGN.md`) and name it in the brief as fixed. Gate design items on the design kit's screenshot quality check, plus owner review of the screenshots where taste decides.

## Handoff to a loop

The brief is the contract for the [work-loop](../work-loop/SKILL.md) skill or any other do-work/check-work loop. The loop should, on every iteration: re-read INTENT.md, work on the next unmet Done item, run its evidence check, and tick it only with evidence. It ends only when every Done item passes, or when a Never/Stop-and-ask condition is hit, and reports remaining items honestly.

## Relationship to other skills

- **Grill Me** (separate skill, if you have it) stress-tests a plan or decision and goes deep. Use Intent Brief instead when the goal is to hand off execution with minimal constraint.
- **Universal Planner** (separate skill, if you have it) builds full durable plans. Use it when work is multi-session, has real dependencies between packets, or needs QA before execution. An INTENT.md can be its starting brief.
