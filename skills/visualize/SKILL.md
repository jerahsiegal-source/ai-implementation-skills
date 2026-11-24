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
- **Look:** Studio by default (`<html data-look="studio">`). Paper and Night are ready in `family.css`. A project's `DESIGN.md` brand overrides the tokens (`--accent`, `--ok`, fonts); keep the structure.
- **Drop the prototype bar.** Example pages carry `data-proto` to show a format and look switcher; real output does not.
- **Every page has, in order:** health word and date, a short title, the verdict as one line under it, the Needs-you panel if anything needs the user, then the blocks.
- **Short copy.** Titles are names of 1 to 6 words. Captions are one line or none. No sentences explaining the page. Follow the floor's copy rules.
- **Status** is always icon plus word (Done, In progress, Next, At risk), never color alone.
- **Detail:** hide it behind a click (expand, tab, drawer), never drop it. Every claim gets a source tag.
- **Charts:** pick the chart by the relationship shown (change over time, ranking, part of whole, flow). Label directly; honest scales. Follow `../chart/SKILL.md` when it is installed.

## 4. Check it

Run the [quality check](../design-kit/quality-check.md): render at about 1280px and 400px, in the chosen look, and fix what fails, at most twice. Confirm no sideways scroll on phone and no console errors.

## Reply

5 lines or fewer: the page path or link, the verdict, what needs the user, and the next step.
