# Design Kit

Shared building blocks for the design skills. You never call this folder directly. `design`, `explore`, `flow`, `chart` and `visualize` read from it, so each rule is written once.

It has no `SKILL.md` on purpose, so Claude Code and Codex do not list it as a command.

| File | What it holds | Read when |
|---|---|---|
| [floor.md](floor.md) | Readability, accessibility, honest data, anti-slop, copy rules, rule order | Every time |
| [quality-check.md](quality-check.md) | The screenshot checklist before handing work back | Before handing back |
| [brand-intake.md](brand-intake.md) | How to turn any brand guide into a project `DESIGN.md` | A brand guide is supplied |
| [styles/](styles) | Named looks with tokens and "best for" | Choosing a look |
| [personal-template/](personal-template) | The starter for your private taste folder | First-time setup |

## Three layers

1. **This repo**: generic skills and defaults anyone can use.
2. **Your personal folder** at `~/.ai-skills/personal/`: your taste and approved styles. It stays on your computer, Claude Code and Codex both read it, and it is never committed.
3. **The project's `DESIGN.md`**: one project's brand, chosen look and page notes. It lives in that project's repo.

Keep the skill folders and this kit side by side (the install scripts do this), because the skills find the kit at `../design-kit/`.
