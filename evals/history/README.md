# Lab history

One file per lab run: `<date>-<model>-<tool>.json`, written by `skills/skill-review/scripts/record.mjs` from a finished [combo test](../combos) run. Comparing files shows whether each skill still beats plain Claude as models change.

Each arm records: checker FAIL and WARN, tokens and seconds, the blind judge's mean score (1 to 5), and its result against plain Claude (`win`, `tie` or `loss`, with `clear` or `slight`). With two independent judge shuffles, `holds` says whether the result held both ways. Only a win that holds counts.

No personal data goes here. Real-use ratings stay in `~/.ai-skills/personal/`.
