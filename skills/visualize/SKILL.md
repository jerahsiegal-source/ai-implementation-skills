---
name: visualize
description: Turn a big output (status, research, a plan, a system, decisions) into one interactive HTML page with the answer first and every detail one click away. Use only when the user types /visualize or $visualize.
disable-model-invocation: true
---

# Visualize

Turn work the user would otherwise have to read into a page they can take in at a glance: the answer in 5 seconds, scannable sections, and full detail behind clicks with a source on every claim.

Standalone. It needs only the shared kit: [floor](../design-kit/floor.md), [craft](../design-kit/craft.md) and [quality check](../design-kit/quality-check.md). Read those, plus `DESIGN.md` in the project and `~/.ai-skills/personal/taste.md` if they exist. The user's words now win over all of them.

## 1. Gather the real content

- Collect what the page is about: the conversation, `INTENT.md`, `handoff.md`, git log, PRs, research notes, files the user names.
- Never invent numbers, dates, sources or status. If something is unknown, show it as unknown.
- Find the **verdict**: one sentence that answers "so what?". Find what **needs the user** (decisions, approvals, blockers).

## 2. Pick the blocks

Formats are building blocks, not templates. Pick by the question the page must answer. Working examples live in [blocks/](blocks/); open them, copy their structure, and replace the data.

| Question | Block | File |
|---|---|---|
| Where are we? (one project, short update) | Health Brief | `blocks/health-brief.html` |
| What is moving, what is stuck? (many workstreams) | Pulse Board | `blocks/pulse-board.html` |
| What did the research find? | Insight Tabs | `blocks/insight-tabs.html` |
| What do you recommend, and why? (argued write-up, comparison) | Margin Notes | `blocks/margin-notes.html` |
| How does it connect? (systems, complex workflows, multi-step updates, dependencies) | Mission Map | `blocks/mission-map.html` |
| What do you need from me? | Decision Desk | `blocks/decision-desk.html` |

- **One question:** one block.
- **A big or many-sided project:** combine. Use the [combined page](blocks/project.html): one header, one Needs-you list, then each block as a tab. Pick only the tabs the project needs.
- **Complex workflows and systems:** lead with the Mission Map.
- **Nothing fits** (a deck, a timeline, a calendar, a funnel): invent a new block. It must reuse the family: the tokens and components in `blocks/family.css`, the icons and status words in `blocks/ui.js`, the Needs-you panel and the drawer. Decks are full-screen sections with arrow-key paging; timelines are the Pulse Board's time axis or the dated list in its Tonight card.

## 3. Build it

- **One self-contained HTML file**: inline `family.css`, `ui.js`, the drawer part of `family.js` and the content. No build step. Save it to `./visualize/<topic>.html` unless the user names a place, or publish it where the tool offers pages.
- **Look:** Studio by default (`<html data-look="studio">`). It switches to dark colors when the viewer's device is in dark mode; keep that. Paper and Night are ready in `family.css`. A project's `DESIGN.md` brand overrides the tokens (`--accent`, `--ok`, fonts); keep the structure.
- **Drop the prototype bar.** Example pages carry `data-proto` to show a format and look switcher; real output does not.
- **Every page has, in order:** health word and date, a short title, the verdict as one line under it, **what to do** (below), then the blocks as evidence.
- **What to do comes first.** If the page asks the user to decide or act, the actions or decision options themselves sit right under the verdict, not a banner pointing further down. Each one shows its size worked out from the data ("+$385 a week", "saves 2 hours a sprint") and a recommended pick. Charts, tables and detail come after, as the evidence for them.
- **Phone first screen:** at about 390px the verdict and the actions fit on the first screen. Keep the whole page short on phone: collapse long charts and tables behind a tap rather than stacking them.
- **Short copy.** Titles are names of 1 to 6 words. Captions are one line or none. No sentences explaining the page. Follow the floor's copy rules.
- **Status** is always icon plus word (Done, In progress, Next, At risk), never color alone.
- **Detail:** hide it behind a click (expand, tab, drawer), never drop it. Every claim is traceable to a source, but keep tags light: one per section or card, or a small footnote link, not a pill on every line.
- **Actions and decisions are different.** An action is something to do; a decision is a real choice that is open in the source. Never turn a blocker or a task into a choice the source doesn't contain.
- **Facts vs guesses.** Every date, number and status comes from the source, with a pointer (file and line, link, or command). Anything you inferred is labelled as inferred ("about", "inferred from…"), never shown as fact.
- **Fact check before you finish:** list every fact on the page with its source pointer and confirm each one against the source. Show the count ("16 facts checked, 0 problems").
- **Numbers:** recompute every number you quote in text from the data before publishing. Don't round two different values into "about the same".
- **Charts:** pick the chart by the relationship shown (change over time, ranking, part of whole, flow). Label directly; honest scales. Follow `../chart/SKILL.md` when it is installed.

## 4. Check it

Run the [quality check](../design-kit/quality-check.md): render at about 1280px and 400px, in the chosen look, and fix what fails, at most twice. Confirm no sideways scroll on phone and no console errors.

## Reply

5 lines or fewer: the page path or link, the verdict, what needs the user, and the next step.
