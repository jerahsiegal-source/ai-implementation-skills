# Chart rules

Each rule has a tag:

- **[R] Research:** backed by perception studies. Never bend.
- **[P] Practice:** what strong data teams agree on. Bend only with a reason you say out loud.
- **[T] Taste:** house style. The project's `DESIGN.md` or the user's taste may override.

A brand or a user ask can change [T] rules. Nothing changes [R] rules or the honest-data rules in the [floor](../../design-kit/floor.md). If the user asks for something that breaks one, do it their way only after saying in one line what it costs.

Where a rule has a check, `check-chart.mjs` or `check-palette.mjs` tests it. The check id is in brackets.

## Truth

- **C1 [R] Bars start at zero.** Length is the value. If zero hides the change, use dots or a line. [bar-baseline]
- **C2 [R] One scale per chart.** No dual y-axes; use two charts side by side. [dual-axis]
- **C3 [P] Line charts may start above zero** when the change is the point, but the axis says where it starts.
- **C4 [R] Position and length beat angle, area and color** for comparing values. Prefer bars and dots to pies, bubbles and heat colors when the exact comparison matters.
- **C5 [P] Same thing, same scale.** Small multiples share one scale. Charts on one page that show the same measure use the same scale.
- **C6 [P] Show the source and date** under every chart with real data. Example data says so.
- **C7 [P] Don't hide the denominator.** Show rates with their counts when counts are small.

## Reading

- **C10 [P] The title is the takeaway, in 10 words or fewer.** "Reply time fell below target in week 9", not "Reply time" and not a paragraph. No subtitle that repeats it. [takeaway] [long-titles]
- **C11 [P] Label directly.** Put series names at the end of lines and values at the end of bars. A legend only when direct labels won't fit.
- **C12 [P] Sort bars** by value unless the categories have a natural order (time, size bands, steps).
- **C13 [P] Horizontal labels.** Never rotate text; flip to a horizontal bar chart or shorten labels. [rotated-labels]
- **C14 [R] No overlapping or cut-off labels** at desktop or phone width. [label-overlap] [label-clipped]
- **C15 [P] Chart text 12px or larger**, never under 11px. [tiny-chart-text]
- **C16 [T] Few gridlines**, light, on the value axis only. No chart borders, no background fills.
- **C17 [P] Round to what matters.** 3.1 h, not 3.1416 h. Same decimals across a series. Never round so far that values the takeaway compares look the same (867 and 925 both shown as "0.9k"); keep that precision on phone labels too.
- **C18 [P] Tabular numbers** wherever digits line up.

## Color

- **C20 [R] Marks need 3:1 contrast** with the background. [mark-contrast]
- **C21 [R] Never color alone.** Every series is labeled or shaped too, so color-blind readers can tell them apart. [cvd-*]
- **C22 [P] Highlight, don't decorate.** One or two colors for what matters, gray for context. [too-many-colors]
- **C23 [P] Color means one thing per page.** If blue is "this year", it is this year in every chart.
- **C24 [P] Sequential data gets one hue light to dark. Data with a meaningful middle gets a diverging scale.** No rainbow scales.
- **C25 [T] Flat fills.** No gradients, shadows, glow or 3D on marks. [gradient-marks] [mark-effects]

## Access

- **C30 [R] Every chart has a non-visual path:** `role="img"` with an `aria-label` that states the takeaway, plus the data as a table (behind "Show data" is fine). [text-path]
- **C31 [P] Hover details are also reachable by keyboard** (focusable points) and never hold information that appears nowhere else.
- **C32 [P] Respect reduced motion.** Animate only to explain a change.
- **C33 [P] Works on a phone.** Charts resize to the container; long category lists become horizontal bars.

## Honesty about the work

- **C40 [R] Never claim a chart was checked or looked at when it wasn't.** Report each check as run, failed or skipped.
- **C41 [R] Never invent data.** Missing values show as gaps and are called out.
