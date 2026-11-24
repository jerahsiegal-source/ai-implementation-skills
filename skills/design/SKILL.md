---
name: design
description: Apply a consistent, high-quality design approach (taste, hierarchy, restraint, brand) to any UI, page, mockup or visual HTML output. Use only when the user types /design or $design.
disable-model-invocation: true
---

# Design

A taste contract, not a design process. Apply settled preferences to whatever is being built. Do not interview the user, research competitors, or generate a design system unless they ask. Those are other skills' jobs.

## 1. Load context (quietly)

Read these, in rule order. Higher wins when they disagree.

1. **The user's message.**
2. **The project:** `DESIGN.md` at the project root (or `.design/DESIGN.md`). If the user supplied a brand guide and there is no `DESIGN.md`, follow [brand intake](../design-kit/brand-intake.md) to write one, and say so in one line.
3. **Personal taste:** `~/.ai-skills/personal/taste.md` and `~/.ai-skills/personal/styles/`. If they don't exist, use the kit defaults and, at the end, offer once to set them up.
4. **The kit:** always read [the floor](../design-kit/floor.md) and [craft](../design-kit/craft.md). Read [styles](../design-kit/styles/README.md) only when choosing a look.
5. **Existing code:** theme files, tokens, component library, CSS variables. Reuse them. Never start a second design system next to an existing one.

If `INTENT.md` exists for this work, its Done and Never items outrank everything except the user's message.

## 2. Name the surface

Decide what kind of screen this is and read only that section of [surfaces](references/surfaces.md): landing page, app dashboard, form or setup flow, results and analytics, HTML report, component mockup, or slides. One product has many surfaces. Its home page and its dashboard follow the same taste but get different density and layout.

If `DESIGN.md` has a **Pages** note for this page, it overrides the surface defaults.

## 3. Choose the look

- `DESIGN.md` names a style: use it.
- Otherwise use the personal default style, or pick by fit from personal approved styles first, then kit styles.
- Nothing fits: invent a style, name it, and say why in one line.
- **Director mode (default):** build the default look. If a different look would clearly serve the product or audience better, propose it in one line. Don't build both unless asked. If `taste.md` says `strict`, skip the proposal.
- Write the tokens first, at the top of the CSS or theme file: 4 to 6 colors with roles, 2 to 3 type roles, a spacing scale, and a radius. Everything after uses the tokens.

## 4. Taste

- **Visual first.** Show it with layout, numbers, charts, icons and diagrams before adding words.
- **One focal point per view.** Decide what the eye hits first and make everything else quieter.
- **Hierarchy by size, weight and space,** not by boxes and color everywhere. Use borders, fills and shadows only where they mark a real group.
- **Restraint.** Fewer elements, shorter copy, no decoration that carries no meaning. Cut before you add.
- **Density fits the job.** Airy for stories and landing pages, packed but ordered for dashboards. "Avoid clutter" means no noise, not no data.
- **One bold move.** Put the distinctive choice in one place, such as the type, a color or the hero number, and keep the rest calm.
- **High level first, detail on demand.** Summaries up top, detail behind tabs, toggles or expanders.
- **Real content.** Use the user's real data and words. Label example data as example data.
- **Every state.** Empty, loading, error, hover, focus and disabled all look designed.
- **Phone and desktop.** Both work. For HTML meant for viewing, support light and dark.
- **Plan before code.** Write the plan first: 4 to 6 named colors, the type pair, the layout idea in one line, and the one bold move. Then ask: would this plan fit any other product in this category? If yes, change the generic part before building. After building, run the swap test in the [quality check](../design-kit/quality-check.md).

## 5. Add-ons

These are separate skills the user can type. When the job clearly needs one and it is installed next to this skill, read its `SKILL.md` and apply it. Say which one you pulled in, in one line.

| The job has | Read |
|---|---|
| Charts, metrics, tables of numbers | `../chart/SKILL.md` |
| A multi-step flow, forms, navigation, "can users finish this?" | `../flow-ux/SKILL.md` |
| A request for options, research or "show me directions" | Suggest `/explore` and stop. Don't run five concepts unasked. |

If an add-on isn't installed, apply the floor and carry on.

## 6. Check

Run the [quality check](../design-kit/quality-check.md): render it, screenshot desktop and phone, fix what fails, look once more. Inside a work loop, those screenshots are the evidence for each design item.

## 7. Save decisions

- When the user approves a look or page treatment for this project, update `DESIGN.md` (**Look** and **Pages** only).
- When the user says "save this style", write it to `~/.ai-skills/personal/styles/<name>.md` in the kit's style format.
- Never write personal taste or a client's brand into the skills folder or repo.

## Reply

Keep it short: what was built and where, the look used and why (one line), any exception proposed (one line), screenshot paths, and anything that failed the check. No design essay.
