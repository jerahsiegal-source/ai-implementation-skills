# Work Loop

Give it an `INTENT.md` and it will work, check, self-review, and fix until **every** done item passes with real evidence. Then it hands back a branch plus a review package. It finishes the whole job instead of stopping at the first slice, and it has stop rules so it doesn't spiral.

## How it works

1. **Setup:** turns each Done item into a tracked check (`loop/done.json`), creates a branch, and records a test baseline.
2. **Build loop:** one item at a time. Make the change, run the item's check, run the regression check, then commit. After 2 failed attempts on an item, it marks the item blocked and moves on.
3. **Review:** a fresh reviewer subagent checks the work against the intent using [the reviewer brief](references/reviewer-brief.md). The worker never reviews its own work. At most 3 rounds.
4. **Finish:** writes `loop/handoff.md` with the evidence, the decisions it made, follow-ups, a prompt for a cross-model review, and a checklist for testing by hand.

Ground rules: evidence or it didn't happen, check things the way the owner would by hand, no fake or weakened tests, never deploy to production.

## Use it

Write the brief first with [Intent Brief](../intent-brief). Then, in Claude Code or Codex, start it under `/goal` so it keeps going across turns:

```
/goal Run the work-loop skill on ./INTENT.md until every done item passes with evidence, or a stop report is printed.
```

Without `/goal`, just say *"Run the work loop on INTENT.md."*

Best for big features or fundamental changes you want finished in full. Not for exploratory or taste-driven work such as picking UI styles.

## Install

- **Claude Code:** copy this folder to `~/.claude/skills/work-loop/`.
- **Codex:** copy this folder to `~/.codex/skills/work-loop/`.

---
Built by [Jerah Siegal](https://www.linkedin.com/in/jerah-siegal-ai-tech/) · MIT License
