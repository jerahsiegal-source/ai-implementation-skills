# Design

Your design taste in one command. Type `/design` (Claude Code) or `$design` (Codex) with any UI, page, mockup or visual HTML task, and it applies the same principles every time: visual first, one focal point, restraint, honest data, readable for everyone. It still adapts to each product and brand.

## How it decides

1. What you say now
2. The project's `DESIGN.md` (its brand and chosen look)
3. Your personal taste in `~/.ai-skills/personal/` (private, never committed)
4. The shared [design kit](../design-kit) defaults and styles

It knows the difference between a landing page, a dashboard, a setup flow and a report, so the same taste gives each one the right density and layout.

## Works with

- `/explore`: five directions to pick from before you build
- `/flow-ux` and `/chart`: deeper UX and data-viz rules (it pulls them in when the job clearly needs them)
- `intent-brief` and `work-loop`: the loop builds against `DESIGN.md` and uses this skill's screenshot check as evidence

## Examples

```
/design Turn this research into a clean one-page HTML report.
/design Redesign the settings page. Keep every feature.
/design Here's our brand guide (brand.pdf). Build the pricing page.
```

## Install

Run the repo's install script so this skill sits next to `design-kit/`. See the [main README](../../README.md#install).

---
Built by [Jerah Siegal](https://www.linkedin.com/in/jerah-siegal-ai-tech/) · MIT License
