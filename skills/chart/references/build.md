# Build the chart

## Stack

1. **Use what the project already uses** (its chart library, its components). Follow its patterns.
2. **Otherwise, for a page or report:** inline SVG with the helpers in [templates/charts.html](../templates/charts.html) (scale, nice ticks, data table, keyboard-reachable tooltip). No dependencies, works offline, and the checker can see inside it.
3. **For many charts or complex interaction:** a library that draws SVG, loaded at a pinned version: Observable Plot, Vega-Lite or D3. Avoid canvas-only libraries unless there are thousands of points; the checker can't read inside a canvas.

## Structure every chart uses

```html
<figure data-chart="bar" data-y-min="0" data-series="1">
  <h2>Billing questions are the biggest share of open tickets</h2>   <!-- takeaway title -->
  <svg role="img" aria-label="Bar chart of open tickets by topic. Billing 61, Login 38, ..."></svg>
  <span class="source">Source: Zendesk export, 18 Nov 2026</span>
  <details><summary>Show data</summary><table>...</table></details>
</figure>
```

- `data-chart` is the form (`line`, `bar`, `column`, `scatter`, `pie`, `area`, `dot`, `histogram`, `map`, `table`).
- `data-y-min` is where the value axis starts. `data-y2` marks a second axis (avoid it). `data-series` is the number of series or slices.
- These attributes let `check-chart.mjs` test the truth rules. Keep them accurate.

## Layout

- Give SVG a `viewBox` sized to its container and redraw on resize. Leave margin for the outermost labels.
- Put the value at the end of each bar and the series name at the end of each line.
- On phones, fewer ticks, shorter labels, and horizontal bars for categories.
- Colors come from CSS tokens (see [color](color.md)) so both themes work. Redraw when the color scheme changes.

## Interaction

- Hover and focus show the exact value. Points are focusable with a visible focus ring.
- Filters and toggles change the chart in place and say what changed.
- Nothing important lives only in a tooltip.
