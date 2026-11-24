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
| [design](skills/design) | Applies one consistent design taste to any UI, page, mockup or visual HTML, while following each project's brand | _LinkedIn post coming_ |
| [explore](skills/explore) | Researches standout examples, shortlists concepts with you, then builds and critiques the best directions side by side | _LinkedIn post coming_ |
| [visualize](skills/visualize) | Turns a big answer (status, research, a system, decisions) into one interactive page: verdict first, detail on click, sources on every claim | _LinkedIn post coming_ |
| [flow-ux](skills/flow-ux) | Walks through a user flow like a real person, ranks what blocks them with a screenshot for each, and fixes the worst on request | _LinkedIn post coming_ |

**The two work as a pair:** Intent Brief defines *what* and *why*, and Work Loop gets it to done. They run in Claude Code and Codex.

**The design skills share one kit.** `design`, `explore`, `visualize` and `flow-ux` read from [design-kit](skills/design-kit) (readability floor, copy and anti-slop rules, styles, brand intake, screenshot check), so the rules are written once. Every one of them, and Work Loop, runs the kit's check, critique and fix round before calling visual work done. `chart` (data viz) is coming next.

**Not sure which to use, or whether Work Loop is worth it?** See [Using the skills together](workflows/design-skills-workflow.md), with test results.

How they fit together on a big design job:

```
intent-brief  ->  explore (you pick a look)  ->  work-loop builds it with design  ->  visualize the handoff
```

All of them are called by name only (`/design` in Claude Code, `$design` in Codex). None run on their own.

<!-- Add one row per skill, e.g.
| [linkedin-post-drafter](skills/linkedin-post-drafter) | Turns rough notes into a LinkedIn post in your voice | [Post](https://www.linkedin.com/posts/...) |
-->

## Install

Clone the repo once, then run the install script. It links every skill into both Claude Code (`~/.claude/skills/`) and Codex (`~/.agents/skills/`, where current Codex looks for personal skills), so they work in all your projects and a `git pull` updates them everywhere.

```bash
git clone https://github.com/jerahsiegal-source/ai-implementation-skills.git
cd ai-implementation-skills
./install.sh            # Mac / Linux
.\install.ps1           # Windows PowerShell
```

The design skills must sit next to `design-kit/`, which the script handles. To copy instead of link, use `./install.sh --copy` or `.\install.ps1 -Copy`.

**Claude.ai / Claude app:** zip a skill folder and upload it under Settings, Capabilities, Skills. For design skills, put a copy of `design-kit/` inside the zip.

### Your personal layer stays private

The install script also creates `~/.ai-skills/personal/taste.md` on your computer. Put your own design taste and approved styles there. Both Claude Code and Codex read it, and it is never part of this repo. Each project's brand lives in that project's own `DESIGN.md`.

Every skill folder has a `SKILL.md` with its instructions and a short README with examples.

## Repo layout

```
skills/            one folder per skill (SKILL.md + README + any scripts or templates)
skills/design-kit/ shared rules and styles the design skills read (not a command)
install.sh / .ps1  link the skills into Claude Code and Codex
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
