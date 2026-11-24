# Craft

The concrete moves that separate "decent AI visuals" from work a good studio would ship. The floor keeps work usable. This file makes it good.

## Type
- Two families at most: one with character for display, one quiet for body. A third only for numbers or code.
- Set a scale and keep to it (for example 14 / 16 / 20 / 28 / 40 / 64). Size jumps should be obvious, not 2px apart.
- Headings are tighter (line height 1.1 to 1.2, slight negative letter spacing on large sizes). Body is looser (about 1.5).
- Use weight and size for hierarchy before color. Two weights per family is usually enough.
- Use tabular numbers wherever digits stack or update.
- Don't use font defaults by accident. Choose a font, and give it a real fallback.

## Space
- Use one spacing scale (4 / 8 / 12 / 16 / 24 / 32 / 48 / 64). No random values.
- Related things sit close together and groups sit far apart. Whitespace does the grouping before any box does.
- Align everything to a few strong edges. Shared left edges read as calm; ragged starts read as messy.
- Build cards in a row with identical padding, baselines and heights driven by content.

## Color
- Neutrals carry 80 to 90% of the page. Tint them slightly toward the accent instead of using flat grey.
- One accent, used with intent: the main action, the key number, the current state. If everything is accented, nothing is.
- Keep status colors (ok, warn, bad) separate from the accent, always with an icon and a word.
- Design dark mode on purpose. Don't just invert: lift surfaces in steps and soften the accent.

## Surfaces
- Pick one depth language per page: hairline borders, or soft shadows, or tonal fills. Don't mix all three.
- Corner radius scales with size (small chips are tighter, big panels softer), and is the same within a role.
- Not everything needs a card. Use cards for things that are separate objects, and plain layout for everything else.

## Data
- The number that matters is the biggest thing in its area, with its label and a comparison (vs last week, vs target).
- Put the takeaway sentence above the chart. The chart is the evidence.
- Strip chart junk: light or no gridlines, no 3D, no legends when you can label lines directly.
- Sparklines and small multiples beat one big chart for "how is everything doing".

## Detail and reveal
- Every element that can be clicked looks clickable (hover, cursor, affordance) and shows where it leads.
- Reveal detail where it belongs: inline expanders for short text, side drawers for a record, separate sections for deep dives.
- Keep the user's place: opening detail doesn't jump the page, and closing returns them to where they were.

## Motion
- 150 to 250ms, ease-out, for state changes. Nothing bounces unless the brand is playful.
- Animate to explain (a row opening, a number updating), never to decorate. Respect reduced motion.

## Icons and imagery
- Use one icon set, one stroke weight and one size grid. Inline SVG. No emoji as icons.
- Real screenshots, diagrams and data beat stock imagery and abstract blobs.

## The polish pass
Before calling it done, look for: orphaned words in headings, uneven gaps, misaligned baselines, labels truncating, focus rings missing, empty states left blank, and any element that exists only because "dashboards usually have one". Remove that last one.
