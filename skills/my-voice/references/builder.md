# Building the profile

1. Snapshot: `python3 scripts/voice.py snapshot` (copies `profile/` to `versions/<timestamp>/`).
2. Start a **fresh subagent** with the prompt below. Fill in `<HOME>`. If there's no subagent tool, run the prompt yourself, as a separate step, reading only the files it names.
3. When it returns, show the user its "what changed" lines and 2 test pieces, then ask: "sounds like me" or "fix X".

If a write is blocked in the subagent, don't route around it. Tell the user what was blocked and let them decide.

---

## Builder prompt

> Build a writing-voice profile for one person from their saved evidence. Read ONLY files under `<HOME>/corpus/`, `<HOME>/edits/`, `<HOME>/blindtest/*-results.md`, and `<HOME>/rules.md`. Do NOT read `<HOME>/profile/` or `<HOME>/versions/`. Use no other knowledge about the person.
>
> **Exclusions**: samples labeled `AI-written` or `someone else`; text inside NOT-MY-WRITING markers (or the older NOT-HIS-WRITING / NOT-THEIR-WRITING); program-written questions inside applications; first attempts the corpus marks as a misread prompt. Samples labeled `possibly AI-assisted` or `AI-assisted` may show what they send, but never count as voice evidence.
>
> **Weighting, most to least:**
> 1. Recent self-typed samples (last ~12 months) and scenario answers.
> 2. Older self-typed long-form writing (reports, applications): the main evidence for long-form structure and argument. Its tone may be dated; say so.
> 3. Dictated talk (vocabulary and how they explain things, not punctuation), habits (self-description), taste picks with reasons.
> 4. Samples older than ~2 years: stable habits only (punctuation, structure, argument), never tone.
>
> When self-description and real writing disagree, trust the writing and note the gap. User feedback in `edits/` and blind test results override everything: every rejected phrase or giveaway must become an Avoid rule, and every "sounds like me" confirms its patterns.
>
> **Write:**
> 1. `profile/base.md` (under 800 words): Core voice; a Formality by audience table (audience → greeting, register, profanity, typical length, evidence count); Sentence rhythm; Vocabulary; Punctuation and formatting; Delays, apologies and asks; Honesty and commitments; Number density; 8–10 example sentences quoted exactly, with source IDs.
> 2. `profile/mediums/<medium>.md` for each medium with real evidence (email, chat, social, long-form reports, resume, ...), under 300 words each, with medium-specific rules only.
> 3. `profile/lexicon.md`: **Keep** (their real phrases, with source IDs) and **Avoid** (what they rejected, never do, or caught in a blind test).
> 4. `profile/gaps.md`: confidence per medium (high/medium/low, with evidence counts), and what's still unclear, one line each.
>
> Every rule must be concrete enough for a drafting model to follow, and backed by evidence.
>
> **Return only:** (a) at most 5 lines on what changed or was corrected; (b) one confidence line per medium; (c) 2 short test pieces in different mediums, written from the profile alone, for situations not in the corpus, exactly as they should be shown to the user.
