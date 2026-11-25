# Samples: importing real writing

Real writing is the strongest evidence. Ask for it by medium, starting with whatever the profile is weakest on (`profile/gaps.md`). Emails usually matter most.

## Sources

| Source | How |
|---|---|
| Pasted text | Save word for word to `corpus/samples/<channel>-batch-N.md`, one `## ID` section per piece |
| Files (.docx, .pdf, .txt, .md) | `python3 scripts/voice.py import <files> --year YYYY --channel report --author me` |
| Email connector (Gmail, Outlook) | Search **sent** mail only. Ask which threads or people to include or exclude. Save only their messages, cut quoted replies and signatures, one line of context per email. Read only: never send, label, or change anything. Many emails is a good job for a subagent. |
| Screenshots of texts | Transcribe only their bubbles (ask which color is theirs). Mark hidden words with `[brackets]`. |
| Social posts | Paste or export. Strip link URLs from hashtags, but keep the words. |

## Labels (required)

Each piece gets a header line:

```
## E12 | 2026 (Jul 23) | email, scheduling reply to client (to a client) | typed by me
Context: one line in your own words about what they're replying to
```

Author labels: `typed by me`, `AI-assisted`, `possibly AI-assisted: <why>`, `AI-written`, `someone else`.

- Ask the user about anything that reads polished, templated, or unlike the rest. They know.
- If a pasted or imported document mixes in text they didn't write (legal templates, application questions, a friend's writing they posted), wrap it in `<!-- BEGIN NOT-MY-WRITING: reason -->` ... `<!-- END NOT-MY-WRITING -->`.
- Exclude whole pieces someone else wrote. Note the exclusion in `samples/index.md` so it doesn't get re-imported.

## Index

Keep `corpus/samples/index.md` as a table: file, count, years, channel, author mix. Add a line for every exclusion.

## Privacy

- Their words only. Summarize others in one line.
- Replace phone numbers, home addresses, account numbers and ID numbers with `[redacted]`.
- Everything stays in the private data folder, never in a repo.

After a meaningful batch (about 10+ pieces, or a new medium), rebuild (references/builder.md) and show test pieces.
