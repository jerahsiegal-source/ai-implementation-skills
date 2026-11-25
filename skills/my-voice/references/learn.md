# Learning loop

This is what closes the gap after setup. Every edit the user makes to a draft is evidence.

## Trigger

- `/my-voice learn`, or
- `python3 scripts/voice.py status` shows 10+ edits since the last learn. Offer it in one line at the end of a drafting task. Don't interrupt.

## Run (fresh subagent if available)

> Read the edit files in `<HOME>/edits/` newer than `<HOME>/edits/.last-learn` (or all, if that file is missing), plus `<HOME>/profile/`. For each before/after pair, list what changed: words swapped, sentences cut or added, formality, length, greeting or sign-off, facts corrected. Find patterns that show up in 2+ edits, or anything the user stated as a rule. Propose at most 7 profile changes, each as: file, the exact line to add or replace, and the evidence (edit filenames). Never propose a change that one edit alone contradicts. Return only the numbered proposals.

## Approve

Show the proposals as a numbered list. The user approves in one line ("all", "1 3 5", "all but 2"). Apply only the approved ones, then run `python3 scripts/voice.py mark-learned`.

A full rebuild (references/builder.md) also uses every edit. Use learn for quick tune-ups and rebuild after big new evidence.
