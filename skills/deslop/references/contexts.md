# Contexts

The same pattern can be fine in one kind of text and a tell in another. Pass the context to the linter with `--context <type>`; it changes severities as listed here (the exact overrides are in `scripts/rules.json`). If the user didn't give a context, infer it from the text and say your guess in one line.

| Context | Use for | What changes |
|---|---|---|
| `general` | Anything else | Default weights. |
| `resume` | Resumes, CVs, LinkedIn experience sections | Stock verbs alone are fine; 3+ stock verbs opening bullets in a row is **high**. Cliches (W-06) and vague impact (P-06) are **high**. First person (S-14) is flagged. Headings, Title Case and label bullets are fine. |
| `report` | Status reports, summaries, memos, research write-ups | Lists and headings are fine. Summary closers (P-04, S-08), inflated significance (P-03) and section narration (S-09) are **high**. |
| `email` | Emails, cover letters, letters, messages | Openers (P-01) and chatbot leftovers (P-02) are **high**. Markdown (F-08) and emoji are **high**. |
| `social` | LinkedIn, X, Threads, community posts | Hype (P-07), emoji, hashtag walls (F-09), contrast frames (S-02), Q-and-A reveals (S-10), punchy fragments (S-11) and one-line-paragraph drama (S-13) are **high**. Exclamation marks are allowed. |
| `docs` | READMEs, technical docs, code comments, changelogs | Marketing tone (P-07) is **high**. Headings, lists and label bullets are fine. |
| `web` | Landing pages, product pages, About pages, ads | Hype (P-07), vague impact (P-06) and strong LLM words (W-02) are **high**. Headings are fine. |

## Rewrite rules per context

**resume**
- Keep every employer, title, date, tool, number and technology name exactly as written.
- Each bullet needs a concrete object: a tool, system, team, customer or number. If it has none and the text doesn't supply one, add a `[NEEDS SPECIFIC]` marker.
- Vary bullet openings. Some can lead with the result or the object.
- No "I", "my" or "me".

**report**
- Lead with the conclusion or the decision needed. Move it to the top if it is at the bottom.
- Cut closing summaries.
- Numbers keep their units and dates.

**email**
- Plain text: no markdown, no emoji.
- Start with the reason for writing. Cut "I hope this finds you well" unless the user's voice clearly uses it.
- Keep it short. Cut paragraphs that only reassure.
- Keep the greeting and sign-off the author wrote.

**social**
- First line is the actual news or claim, not "Excited to share".
- Keep the author's opinions and first person; that is the point of a post.
- Two or three hashtags at most, at the end.
- Join one-line paragraphs into real ones.

**docs**
- **Never touch** code blocks, inline code, commands, file paths, flags, API names, product names, version numbers or config keys. The linter already skips code; you must too.
- Cut marketing language ("blazing fast", "seamless"). Say what it does.
- Headings and lists that aid scanning stay.

**web**
- Every claim about the product should be checkable: what it does, for whom, a number. Where it isn't, add a marker such as `[NEEDS SPECIFIC: what does it integrate with?]`.
- Testimonials and customer quotes are quoted material: leave the words alone. If a quote looks invented (no name, no company), flag it with `[NEEDS SPECIFIC: real customer and permission?]`; never "improve" it.
