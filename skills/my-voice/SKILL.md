---
name: my-voice
description: Writes emails, texts, posts, reports and applications that sound like the user, from a private voice profile built by interviewing them and reading their real writing. Use for "/my-voice", "write this as me", "in my voice", "sound like me", or to set up, test or improve the profile.
---

# my-voice

Builds a profile of how one person writes, then drafts in that voice and gets better every time they edit a draft.

## Where the data lives

All personal data stays on the user's computer and is never committed or published:

- Default: `~/.ai-skills/personal/my-voice/` (next to the other private skill files)
- Override: the `MY_VOICE_HOME` environment variable
- An older `~/.my-voice/` is still read if the default doesn't exist yet

`python3 scripts/voice.py where` prints the folder in use. On Windows, use `python` or `py` instead of `python3`. Scripts are in this skill's folder.

Run `python3 scripts/voice.py init` the first time to create the layout:

```
my-voice/
  corpus/          raw answers, word for word (talk, habits, scenarios, taste, interview, scenarios-plus)
  corpus/samples/  real writing with labels, plus index.md
  profile/         base.md, lexicon.md, gaps.md, mediums/*.md  (built from corpus, never hand-written)
  edits/           before/after pairs and feedback
  blindtest/       rounds, guesses, keys, results
  evals/           tasks.json and test runs (see tests/README.md)
  versions/        profile snapshots before each rebuild
  rules.md         hard rules the user states (e.g. "never mix my day job into client email")
```

Never copy anything from this folder into a repo, a public page, a shared artifact or a commit.

If no profile exists when the user asks for a draft, say so in one line and offer `/my-voice setup` (about 25 minutes). Draft anyway if they want, and label it as unprofiled.

## Commands

| Command | What it does | Read |
|---|---|---|
| `/my-voice setup` | Quick setup, about 25 min, no samples needed | references/setup-quick.md |
| `/my-voice setup samples` | Import real writing (paste, files, email, screenshots) | references/samples.md |
| `/my-voice setup interview` | 30–40 min: opinions, decisions, how they explain things | references/setup-deep.md |
| `/my-voice setup scenarios+` | 10 more scenarios incl. resume, report, critical feedback | references/setup-deep.md |
| `/my-voice setup blindtest` | 10 pieces, real vs AI; misses become fixes | references/blindtest.md |
| `/my-voice setup crosscheck` | A second model checks the profile against the evidence | references/setup-deep.md |
| `/my-voice rebuild` | Rebuild the profile from the corpus | references/builder.md |
| `/my-voice draft ...` or any "write this as me" | Draft in their voice | references/drafting.md |
| `/my-voice learn` | Turn saved edits into proposed profile changes | references/learn.md |
| `/my-voice status` | What's done, confidence per medium, next step | below |

## Rules for every interview step

1. **Save raw answers word for word**, filler and typos included, the moment they arrive. Never summarize into the corpus.
2. **One question at a time.** Short questions. No example answers shown first. No praise, no recaps between questions.
3. **Voice-friendly.** Answers may be dictated. Keep prompts short enough to read aloud.
4. **Scenarios show the real incoming message** (sender, subject, body) and put the key constraint **in bold inside the prompt**. Vague situations get vague answers.
5. **If an answer doesn't fit the prompt** (e.g. the user misread it), save it anyway, then point out the mismatch in one line and offer a redo. Keep both attempts, labeled.
6. **Label every sample**: `year | channel | typed by me / AI-assisted / AI-written / someone else`. Ask when unsure. Never use AI-written text as voice evidence.
7. **Mark text inside a sample that isn't theirs** (legal templates, application questions, quoted replies) with `<!-- BEGIN NOT-MY-WRITING: reason -->` / `<!-- END NOT-MY-WRITING -->`. The builder also accepts the older NOT-HIS-WRITING and NOT-THEIR-WRITING markers.
8. **Privacy**: save only the user's own words. Summarize other people's messages in one line of context. Redact phone numbers, addresses, account and ID numbers.

## Building the profile

Always build with a **fresh subagent** that reads only the corpus and edits (not the old profile, not this conversation). This gives a clean read of the evidence. Snapshot the current profile to `versions/` first. Full instructions and the weighting rules are in references/builder.md.

No subagent tool (some Codex and Claude app setups)? Do the build yourself as a separate step: re-read only the corpus files, ignore what you remember from the interview, and follow references/builder.md exactly.

After every build, write **2 short test pieces** from the profile alone and ask: "sounds like me" or "fix X". Save the answer to `edits/`.

## Drafting

Follow references/drafting.md. The short version:

1. Read `profile/base.md`, `profile/lexicon.md`, `rules.md`, and the one `profile/mediums/*.md` that fits.
2. Match the audience row in the formality table. Use their real phrases where they fit. Nothing from the Avoid list.
3. **Never invent facts, excuses, events or numbers** the user didn't give. Ask, or leave it general.
4. **Final check with deslop's linter**, if the deslop skill is installed: lint the draft and fix only real AI tells, in their voice.
5. **Polish reports and long emails** with a deslop rewrite pass, then re-check against the profile. Never for texts or posts. "polish" / "no polish" overrides.
6. Return the draft only, ready to paste. No preamble.

When the user edits a draft or says what's off, save the before/after with `python3 scripts/voice.py log-edit`. After 10 new edits, offer `/my-voice learn`.

## Status

`python3 scripts/voice.py status` prints: corpus files and word counts, samples by channel and author label, profile age, edits since last learn, last blind test score. Show it as a short checklist with a confidence level per medium (read `profile/gaps.md`), then suggest the single most useful next step:

- No profile yet → quick setup
- Fewer than ~10 real samples → samples
- Never blind-tested → blindtest
- 10+ unprocessed edits → learn
- A medium marked low confidence that they use → scenarios+ or samples for that medium

## Testing it

`tests/voice_eval.py` checks whether drafts beat plain Claude, using the user's own held-out writing as the answer key. Results stay in the private folder. See tests/README.md.
