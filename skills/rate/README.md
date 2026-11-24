# Rate

Two seconds after a skill finishes: was it right the first time?

```
/rate y
/rate n too long
/rate n wrong chart type
```

Claude fills in which skills ran, the model and how many fixes it took, then adds one line to `~/.ai-skills/personal/usage-log.jsonl` on your computer. Nothing goes in the repo.

You don't have to rate every use. [`/skill-review`](../skill-review) also reads your Claude Code and Codex history and guesses from your follow-ups. A `/rate` just replaces the guess with your answer.

---
