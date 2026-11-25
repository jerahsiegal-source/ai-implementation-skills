# Blind test (about 10 minutes)

Measures whether the profile can pass as the user. Each miss becomes a fix.

## Build the round (fresh subagent)

> Build a blind test. Real samples: `<HOME>/corpus/samples/`. Profile: `<HOME>/profile/` (base.md, lexicon.md, mediums/*.md).
>
> 1. Pick 5 REAL excerpts labeled `typed by me`. Never use AI-labeled pieces, NOT-MY-WRITING text, scenario answers, or sentences quoted in the profile. Prefer older or routine pieces the user is least likely to remember. Mix mediums. 30–90 words each, cut only at sentence boundaries, words unchanged, typos kept. Replace names of people and companies with placeholders like [Client].
> 2. Write 5 AI pieces from the profile only, matching the same mix of mediums and lengths, for similar but different situations. **Do not invent personal events or excuses** beyond what the profile supports. Do your honest best to make them indistinguishable.
> 3. Shuffle into a random order, numbered 1–10, with no pattern.
> 4. Write `<HOME>/blindtest/roundN.md` (pieces plus a neutral one-line label each, no answers) and `<HOME>/blindtest/roundN-key.md` (REAL with source ID, or AI with the situation).
>
> Return only the contents of roundN.md.

Don't read the key until all guesses are in.

## Run it

- Show 5 pieces at a time (easier to read). Ask for `1 ME, 2 AI, ...`, reasons optional.
- Save guesses word for word to `blindtest/roundN-guesses.md`.
- If every real sample came from this session, say so: recognizing your own fresh writing is easier than it will be later.

## Score and fix

1. Show a short results table: #, type, actual, their guess, ✅/❌.
2. Headline: how many AI pieces **passed as them** (the number that matters).
3. Ask what gave away each AI piece they caught. A few words each is enough.
4. Save the reasons word for word to `blindtest/roundN-results.md`.
5. Turn each reason into a concrete rule:
   - Specific phrases → lexicon Avoid
   - Invented facts or context → "never invent" rule in base.md, plus `rules.md` if it's a hard boundary (e.g. keep work worlds separate)
   - "Too stiff / too technical / too many numbers" → a measurable rule (e.g. at most 1–2 figures per sentence)
6. Add the rules to the profile now. They also feed the next full rebuild, since the builder reads blind test results.

Run a new round after about 20 edits or a rebuild. Goal: AI pieces pass as them at least 3 times out of 5.
