---
name: rate
description: Log whether the last skill output was right the first time, to a private file on this computer. Use only when the user types /rate or $rate, for example "/rate y" or "/rate n too long".
disable-model-invocation: true
---

# Rate

Record one line about the work just done, so `/skill-review` can track how often skills get it right the first time. It takes two seconds and must stay that way.

## Read the user's words

- `y`, `yes` or a score of 4 to 5: right the first time.
- `n`, `no` or a score of 1 to 3: it needed fixes.
- Anything after that is the note. Keep it word for word, max 200 characters.
- Nothing after `/rate`: ask once, "Right first try? y or n", and stop.

## Fill in the rest yourself

- **Skills:** the skills used for the work being rated, usually the most recent `/name` or `$name` in this conversation, plus any it called. If none were used, use `none`. That still counts: it is the plain-Claude baseline.
- **Fixes:** how many times the user asked for a change to that work before this rating. Count only asks to change it, not new tasks.
- **Model** and **tool** (`claude-code`, `codex` or `claude-app`): from what you know about this session. Leave the model out if you are not sure.

## Write it

Run, from this skill's folder:

```
node scripts/rate.mjs --first-try y --skills design,chart --fixes 0 --note "short note" --model <model> --tool claude-code
```

It appends to `~/.ai-skills/personal/usage-log.jsonl`. Never write the rating anywhere in a repo. If Node or the shell isn't available (for example in the Claude app), show the JSON line from the script's format and ask the user to keep it, then stop.

## Reply

One line, for example: `Logged: design · needed fixes · too long`. No other comment, and don't redo the work unless asked.

---
Created by Jerah Siegal · https://www.linkedin.com/in/jerah-siegal-ai-tech/ · MIT License
