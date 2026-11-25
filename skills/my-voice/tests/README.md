# Testing my-voice

Does it actually sound like you, better than plain Claude? This test uses messages you really sent as the answer key.

## Set up once

1. Pick about 10 real messages from your samples, across the mediums you use (email, texts, posts). Prefer ones the profile doesn't quote (search `profile/` for their IDs).
2. For each, write a short brief with only the facts, in plain words, not the original wording.
3. Save them in your private folder as `evals/tasks.json`:

```json
[
  {"id": "e39-order", "medium": "email", "real": "E39",
   "brief": "New email to a rental company's support. Facts: ordered size A, got size B, ..."}
]
```

The test strips those messages from a temp copy of your corpus, so no arm can read the answer.

## Run

```
python3 tests/voice_eval.py run --author "Your Name"
python3 tests/voice_eval.py judge --run <run folder it prints>
```

Add `--model <name>` to test a new model, or `--runner codex` for Codex. Results stay in `<private folder>/evals/runs/`.

## Arms

| Arm | What it is |
|---|---|
| plain | Plain Claude with the brief and your name |
| samples | Plain Claude with all your other real samples pasted in |
| voice | `/my-voice draft`, profile only |
| voice_lint | `/my-voice draft` with deslop installed (lint final check) |
| voice_deslop | The voice draft, then a full `/deslop` pass |

## Judges

Both are fresh models with no skills, shown items in shuffled order.

- **Turing:** your real message next to a draft, both orders. "Which did the person write?" *Fooled* is how often it picks the draft. 50% means it can't tell.
- **Rubric:** all drafts for a task next to your real message. Voice match 1–10, invented facts (count), would-send 1–10, and a best pick.

A model judge is a proxy. The real test is still you: run `/my-voice setup blindtest` after big changes.
