# Chart

Makes charts, metrics and dashboards that make one point clearly and honestly, and checks them before handing them back.

Type `/chart` (Claude Code) or `$chart` (Codex):

```
/chart how reply times changed this quarter, from tickets.csv
/chart a dashboard for these sales numbers
/chart fix the charts on this page
```

`/design` and `/visualize` read this skill whenever a page needs a chart.

## What it does

1. Writes a one-line brief: the takeaway, who reads it, and where it shows.
2. Picks the simplest chart that shows that takeaway ([forms](references/forms.md)).
3. Builds it with a takeaway title, direct labels, the source, accessible colors, and a data table for screen readers ([rules](references/rules.md), [color](references/color.md), [build](references/build.md)).
4. Runs the checks, fixes what fails, and runs them again until they pass.

## The checks

| Script | Checks |
|---|---|
| `scripts/check-chart.mjs page.html` | Takeaway title, text alternative, bars start at zero, dual axes, pie slices, color count, mark contrast, shadows and gradients, rotated, overlapping, cut-off and tiny labels, at desktop and phone width |
| `scripts/check-palette.mjs "#hex,#hex" --bg "#fff"` | Contrast with the background, colors too alike, and pairs that blur together for color-blind readers |
| `../design-kit/scripts/check-page.mjs page.html` | The kit's AI-slop and layout check, with screenshots |

`check-chart.mjs` needs Playwright, like the kit's page check. Run `node scripts/test-checks.mjs` to test the scripts themselves.

## Brand colors

Put a **Chart** section in your project's `DESIGN.md` with your series colors. The skill checks them with `check-palette.mjs` and keeps your main brand color for the highlighted series. Otherwise it uses the default palettes in [color](references/color.md), which already pass the checks in light and dark mode.

## Starter

- [templates/charts.html](templates/charts.html): number tiles, a line chart, a sorted bar chart and small multiples, with no dependencies.
- [templates/dashboard.html](templates/dashboard.html): a small dashboard built with this skill from the eval data, in a brand palette that first failed the color check and was fixed.

Both pass every check.
