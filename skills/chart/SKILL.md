---
name: chart
description: Make honest, readable charts, metrics and dashboards. Pick the right chart for the point, label it directly, use accessible colors, and check it before handing back. Use only when the user types /chart or $chart.
disable-model-invocation: true
---

# Chart

Turn numbers into a chart that makes one point clearly and truthfully. It works on its own or inside `/design`, `/visualize` and the work loop, which read this file when a page needs a chart.

## 1. Load context (quietly)

Read in rule order. Higher wins when they disagree, except that nothing overrides the truth rules.

1. **The user's message.**
2. **The project:** `DESIGN.md` (brand, chart colors, chosen look) and existing chart code or libraries.
3. **Personal taste:** `~/.ai-skills/personal/taste.md`, if it exists.
4. **The kit:** [floor](../design-kit/floor.md) and the Data section of [craft](../design-kit/craft.md).

## 2. Write the brief (one line)

`Takeaway | Audience | Where it shows`

For example: `Reply time fell below target in week 9 | support leads | weekly report page`. Where it shows means page, dashboard, slide, doc or small inline. It sets the size, density and how much text the chart can carry.

Then check the data: its source, units, date range and any gaps. **Never invent or fill in numbers.** If data is missing, show the gap and say so. If there is no clear takeaway, ask one question or pick the most useful reading and say which.

## 3. Pick the form

Use the table in [forms](references/forms.md). Pick by the relationship the takeaway is about. Choose the simplest truthful form. A number tile or a table is often the right answer.

## 4. Build it

- Follow [build](references/build.md): use the project's chart library if there is one, otherwise inline SVG from the [starter](templates/charts.html).
- Every chart gets: a **takeaway title**, **direct labels**, the **source**, `role="img"` with an `aria-label` that states the takeaway, and the **data as a table** behind "Show data".
- Colors from [color](references/color.md). Highlight what matters, gray for context. If colors come from a brand, run `scripts/check-palette.mjs` on them first.
- Apply the [rules](references/rules.md). [R] rules never bend. [T] rules give way to the brand or the user.

## 5. Check, fix, repeat

Run both checkers on the page. From this skill's folder:

```
node scripts/check-chart.mjs <page.html>
node ../design-kit/scripts/check-page.mjs <page.html> --out <folder>
```

- Fix every FAIL. Judge every WARN, and fix it unless there's a reason you can name.
- Run both again until each exits 0. Then look at the desktop and phone screenshots yourself: is the takeaway the first thing you see?
- If Playwright isn't installed, the browser checks are skipped. Say so. Don't claim a check ran when it didn't.
- Inside a work loop, the checker output and screenshots are the evidence for each chart item.

## Reply

Keep it short: where the chart is, the takeaway in one line, the form and why (a few words), the checker summary lines, and anything skipped or left as a WARN with its reason.
