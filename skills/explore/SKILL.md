---
name: explore
description: Research how others solve a design problem, then mock up five genuinely different directions on one comparison page so the user can pick a direction or mix features. Use only when the user types /explore or $explore.
disable-model-invocation: true
---

# Explore

Turn "what should this look like?" into five real options side by side. The user picks; this skill does not build production code.

Built on top of [`/design`](../design/SKILL.md). Read it first, along with its context order: user, `DESIGN.md`, personal taste, [the floor](../design-kit/floor.md). Every direction obeys the floor and the project's brand. The brand fixes the colors. Directions vary everything else.

## 1. Frame (one short message, at most two questions)

State back in two or three lines:
- **What** is being designed (a page, a flow, a report format, a whole look).
- **For whom** and **the one job** it must do.
- **Fixed:** brand, content, features, anything in `INTENT.md` Done or Never.

Ask only if "what" or "for whom" is truly unclear. Otherwise state your reading and go.

## 2. Research (skip if the user says so or there is no web access)

- Look at 5 to 8 real products or sites that solve the same job well. Include at least two from outside the obvious category.
- For each, note the one pattern worth borrowing and link it.
- No web access: say so in one line and work from known patterns, labeled as such.

Keep research to a small table on the comparison page. It feeds the directions; it is not the deliverable.

## 3. Five directions

Vary these axes: **layout idea**, **density**, **type personality**, **color strategy** (within brand), **interaction model** (scroll, tabs, drill-down, canvas, cards...).

Rules:
- Every direction differs from every other on at least two axes. Changing only colors does not count as a new direction.
- Include one **expected** direction (the safe, proven pattern), one **bold** direction (a real risk), and one **borrowed** direction (a pattern from outside the category).
- Start from approved styles in `~/.ai-skills/personal/styles/` and the kit's [styles](../design-kit/styles/README.md) where they fit, but at least two directions should be new.
- All five use the same real content, so the user compares design, not content.
- No direction uses anything from the anti-slop list unless the brand asks for it.

## 4. The comparison page

Build one HTML file at `./explore/<topic>.html` (or the folder the user names). It holds:

- **Top:** the job in one line, then five thumbnails or tabs (A to E), each with a name, a one-line idea, best at, and risk.
- **Each direction:** a working mockup of the key screen at real size. Clickable where interaction is the point.
- **Steal list:** the standout features across all five, as checkable chips (for example "B's status lights", "D's progress ring"), so the user can mix.
- **Research:** the short table from step 2, with links.

Run the [quality check](../design-kit/quality-check.md) on the page itself.

## 5. Pick and record

Ask one question: "Which direction, or which mix?" Then:
- **For a project:** write the choice to `DESIGN.md` (**Look**, and **Pages** if it is page-specific), following [brand intake](../design-kit/brand-intake.md) if the file doesn't exist yet.
- **For your personal style list:** if the user says "save this style", write it to `~/.ai-skills/personal/styles/<name>.md` in the kit's style format.
- **Next step:** hand off to `/design` to build it, or to the work loop if an `INTENT.md` exists. In that case the chosen direction becomes a fixed input to the brief.

## Reply

Under 6 lines: the page path, the five direction names with a few words each, which one you'd pick and why (one line), and the question.
