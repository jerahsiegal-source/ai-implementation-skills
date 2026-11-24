---
name: explore
description: Research standout examples, write 6 to 8 design concepts to shortlist, then build, critique and compare the shortlist so the user can pick a direction or mix features. Use only when the user types /explore or $explore.
disable-model-invocation: true
---

# Explore

Turn "what should this look like?" into a few excellent options side by side, grounded in real research. The user picks; this skill does not build production code.

Built on top of [`/design`](../design/SKILL.md). Read it first, along with its context order: user, `DESIGN.md`, personal taste, [the floor](../design-kit/floor.md). Every direction obeys the floor and the project's brand. The brand fixes the colors. Directions vary everything else.

## 1. Frame (one short message, at most two questions)

Use `/explore` when the look or layout is genuinely open. If the user already has a clear spec and only needs it built, say so in one line and suggest `/design` instead: in tests, exploring a settled spec made the result worse.


State back in two or three lines:
- **What** is being designed (a page, a flow, a report format, a whole look).
- **For whom** and **the one job** it must do.
- **Fixed:** brand, content, features, anything in `INTENT.md` Done or Never.

Ask only if "what" or "for whom" is truly unclear. Otherwise state your reading and go.

## 2. Research (do it unless the user opts out)

Generic output comes from skipping this step. Do it properly.

- Find **10 to 12 standout real examples** that solve the same job: the best-in-class ones in the category, plus at least three from outside it (editorial, data journalism, games, print, physical products).
- **Capture each one.** Take a screenshot (Playwright or the tool's browser) and save it to `./explore/<topic>/refs/`. If you can't capture one, link it and say so.
- For each, write **what makes it great** in craft terms, not adjectives: type pairing and scale, spacing rhythm, color strategy, how it hides and reveals detail, one signature detail.
- No web access: say so, then work from named real examples you know well and label them "from memory".

## 3. Concepts as quick, clickable mockups

Write **6 to 8 concepts**, each in 3 lines: a name, the big idea, and which references it borrows from. Then make each one a **quick but real web page**, not a static sketch or a picture of a page: full width, the user's real content (or a believable stand-in), and the one interaction that defines it working (tabs switch, rows expand, a drawer opens). Rough polish is fine at this stage; the layout, density and feel must be judgeable by clicking around. Cover the spread:
- Every concept differs from every other on at least two of: **layout idea**, **density**, **type personality**, **color strategy** (within brand), **interaction model**.
- Include an **expected** concept (the proven pattern done extremely well), a **bold** one, and a **borrowed** one from outside the category.
- Reuse an existing style only if it truly fits. Recycled looks are not new concepts.

Run the [page checker](../design-kit/scripts/README.md) on every concept mockup and fix its FAILs before showing it (floor problems like overflow and contrast are never part of a concept; WARNs may wait for step 4). Put the concepts on one page next to the reference gallery, each with an "Open full size" link, and ask the user to shortlist **2 to 4**. If they say "you pick", choose the strongest four and say why in one line each. Skip this step only when the user says "just build them".

## 4. Build the shortlist properly

- Take each shortlisted mockup to a **finished, full-size, working page** on the user's **real content**, not a thumbnail and not fake data unless none exists.
- Apply `/design`, the [floor](../design-kit/floor.md), [craft](../design-kit/craft.md) and the user's personal taste.
- Every direction obeys the brand in `DESIGN.md`. The brand fixes colors; directions vary everything else.

## 5. Critique and revise (once)

- Hand the screenshots, the reference gallery and the concepts to a **fresh reviewer**: a new subagent where the tool supports one, otherwise a separate critique pass that starts from the screenshots alone.
- The reviewer first checks the user's **main job**: can they do the main task from a visible button where they'd expect it (on every row, for lists), and does nothing change data without a clear action or confirm? A direction that fails this is fixed before anything else, however good it looks.
- The reviewer scores each direction 1 to 5 on: **would a top studio ship this**, distinct from generic AI output, hierarchy in 5 seconds, craft details (type, spacing, alignment), and fit to the job. It lists the three biggest fixes for each.
- Fix those, re-render, and keep before and after screenshots. One round only; report anything left over.
- Run the [quality check](../design-kit/quality-check.md) on the final pages.

## 6. Compare, pick, record

One HTML file at `./explore/<topic>/index.html` (or where the user says) with:
- **Top:** the job in one line and the shortlist as large previews, each with best at, risk and its critique score.
- **Each direction:** the working page, clickable where interaction matters.
- **Steal list:** standout features across directions as checkable chips, so the user can mix.
- **Research gallery:** the reference screenshots with their craft notes and links.

Ask one question: "Which direction, or which mix?" Then:
- **For a project:** write the choice to `DESIGN.md` (**Look**, and **Pages** if it is page-specific), using [brand intake](../design-kit/brand-intake.md) if the file doesn't exist yet.
- **For your personal styles:** if the user says "save this style", write it to `~/.ai-skills/personal/styles/<name>.md` in the kit's style format.
- **Remember taste:** add what the user liked and rejected, in a line each, under **What I like** / **What I don't like** in `~/.ai-skills/personal/taste.md`, so the next round starts smarter.
- **Next step:** hand off to `/design` to build it, or to the work loop when an `INTENT.md` exists, with the chosen direction as a fixed input.

## Reply

Under 6 lines: the page path, the direction names with a few words each, which one you'd pick and why (one line), and the question.
