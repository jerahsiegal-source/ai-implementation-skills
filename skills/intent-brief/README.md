# Intent Brief

A short interview that turns what you want into a one-page `INTENT.md`: the **outcome**, the **why**, the **done-when gates**, and the **hard limits**. An AI agent can then do the work without you telling it how.

Most handoffs to AI go wrong in one of two ways. You over-specify the how, so the agent can't use its judgment. Or you under-specify what done means, so it stops at slice 1 of 6. This skill fixes both.

## What you get

- 5 to 10 questions, asked a few at a time, about Outcome, Why, Done, Never, and Stop-and-ask
- An `INTENT.md` written in your own words, one page long
- A quick clarity rating, so you get better at describing work over time

It works well with rambling or dictated input. It pulls the general rule out of your examples and turns your complaints into checks.

## Use it

Say something like: *"Let's do an intent brief for the new onboarding flow."*

Then hand the finished `INTENT.md` to the [Work Loop](../work-loop) skill, or to any agent, and let it run.

## Install

- **Claude Code:** copy this folder to `~/.claude/skills/intent-brief/` (or `.claude/skills/` in a project).
- **Codex:** copy this folder to `~/.agents/skills/intent-brief/`. `agents/openai.yaml` sets the display name and turns off implicit invocation.
- **Claude.ai:** zip this folder and upload it under Settings, Capabilities, Skills.

---
Built by [Jerah Siegal](https://www.linkedin.com/in/jerah-siegal-ai-tech/) · MIT License
