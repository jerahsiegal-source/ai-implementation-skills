# Styles

Named looks the design skills can pick from. A style sets colors, type, shape and a few layout moves. It never overrides [the floor](../floor.md) or a project's brand colors. With a brand, the skill keeps the brand's colors and borrows the style's type, density and layout.

## Status

- **candidate**: ships with the kit and works fine, but has not been approved by you.
- **approved**: you like it. Approved styles go in your personal folder (`~/.ai-skills/personal/styles/`), not here, so your picks stay yours.

The skills look in your personal styles first, then here.

## Picking a style

Match **Best for** to the job. If two fit, take the calmer one. If none fits, invent a new style, give it a name, and say why in one line. When you like an invented style, say "save this style" and it is written to your personal folder in this same format.

| Style | Feel | Best for |
|---|---|---|
| [Calm Paper](calm-paper.md) | Light, airy, very readable | Reports, research, long reading, docs |
| [Mission Control](mission-control.md) | Dark, dense, status lights | Engineering status, monitoring, ops dashboards |
| [Bold Brief](bold-brief.md) | Magazine, huge headline, high contrast | Executive summaries, decisions, one-page briefs |
| [Soft Studio](soft-studio.md) | Rounded, friendly, color-tinted | Progress for wider audiences, onboarding, consumer UI |

## Format for a new style

```markdown
# <Name>
Status: candidate | approved
Feel: <three words>
Best for: <jobs>
Not for: <jobs>

## Tokens
light: bg, surface, ink, muted, line, accent, ok, warn, bad
dark: same names
type: display <font>, body <font>, numbers <font>
shape: radius, borders, shadows
density: airy | balanced | dense

## Moves
- <2 to 4 layout or detail moves that make this style recognizable>
```
