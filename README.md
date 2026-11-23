# AI Implementation Skills

**Practical, open source Claude skills and AI workflows from real implementation work.**
Built and maintained by [Jerah Siegal](https://www.linkedin.com/in/jerah-siegal-ai-tech/), AI implementation consultant and founder of Market Fit AI.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Jerah%20Siegal-0A66C2?logo=linkedin)](https://www.linkedin.com/in/jerah-siegal-ai-tech/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Why this repo exists

I spend a lot of my week using AI to do real work: research, marketing for startups, automation, and shipping product. When a workflow keeps paying off, I turn it into a reusable skill and publish it here so anyone can use it, fork it, or improve it.

Each skill is tested on my own work first. Many of them come with a LinkedIn post explaining the problem it solves and what I learned building it.

## Skills

| Skill | What it does | Write-up |
|---|---|---|
| [intent-brief](skills/intent-brief) | A short interview that turns what you want into a one-page `INTENT.md` (outcome, why, done-when gates, hard limits) an agent can execute against | _LinkedIn post coming_ |
| [work-loop](skills/work-loop) | Takes an `INTENT.md` and works, checks, reviews and fixes until every done item passes with real evidence | _LinkedIn post coming_ |

**The two work as a pair:** Intent Brief defines *what* and *why*, and Work Loop gets it to done. They run in Claude Code and Codex.

<!-- Add one row per skill, e.g.
| [linkedin-post-drafter](skills/linkedin-post-drafter) | Turns rough notes into a LinkedIn post in your voice | [Post](https://www.linkedin.com/posts/...) |
-->

## How to use a skill

**Claude.ai / Claude app:** download the skill folder as a .zip and upload it under Settings, Capabilities, Skills.

**Claude Code:** copy the skill folder into `~/.claude/skills/` (personal) or `.claude/skills/` in your project.

**Codex:** copy the skill folder into `~/.codex/skills/`.

Every skill folder has a `SKILL.md` with its instructions and a short README with examples.

## Repo layout

```
skills/            one folder per skill (SKILL.md + README + any scripts or templates)
workflows/         longer how-tos and prompts that are not packaged as skills
posts/             notes and source material behind my LinkedIn posts and videos
```

## Work with me

I help teams figure out where AI actually fits, then implement it.

- **LinkedIn:** [Jerah Siegal](https://www.linkedin.com/in/jerah-siegal-ai-tech/) (I post about how I use AI, new model releases, and what is working)
- **Consulting:** Autom-AI-tion Innovations
- **Product:** Market Fit AI

If a skill helped you, a star on this repo or a comment on the related LinkedIn post means a lot.

## Contributing

Issues and pull requests are welcome. If you have improved a skill or adapted it to a new use case, open a PR and tell me what you changed and why.

## License

[MIT](LICENSE). Use these freely, including commercially. Credit is appreciated but not required.
