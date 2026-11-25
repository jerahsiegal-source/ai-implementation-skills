# Drafting in their voice

## Before writing

1. Read `profile/base.md`, `profile/lexicon.md`, `rules.md`, and the medium file that fits (`profile/mediums/`). If the medium has no file or is marked low confidence in `gaps.md`, use base.md and mention it in one line after the draft.
2. Work out: medium, audience (find the row in the formality table), goal, and the facts you were given.
3. If the user gave a brain dump (dictated, messy), treat it as content, not style. Their dictated phrasing isn't how they type.

## While writing

- Greeting, sign-off, register and profanity come from the audience row. When unsure, go one step more formal than you think.
- Use their real phrases from Keep where they fit naturally. Don't stuff them in.
- **Never invent** facts, events, excuses, numbers, names or commitments. If a reason or date is missing, leave it general or ask. Inventing context is the fastest way to sound fake.
- Follow `rules.md` without exception (e.g. worlds that never mix).
- Follow the number density rule.
- Match their length habits for the medium. Don't pad. A short reply stays short.
- Nothing from Avoid.

## Don't polish them into AI

Blind tests against real messages show the same giveaways every time: the draft is tidier than the person. So:

- **Add nothing they didn't ask for.** No extra closing ask, no "I'll keep you posted", no reassurance line, no thank-you that wasn't in the brief. These count as invented, like facts.
- **Don't mirror the brief's wording.** The brief is a list of facts, not their phrasing. Say it the way they'd type it fast, in the words their profile and samples show.
- **Keep their roughness.** If their profile shows run-ons, small repeats, loose capitalization or a wordier way of saying things, the draft can have them too. Don't tidy what they wouldn't.
- **Greeting and sign-off only when their evidence for that audience has them.** Quick heads-ups and how-to replies to people they work with often skip both.
- **No borrowed color.** Don't add slang, fillers or framing lines to sound casual unless their profile shows them for this kind of person. Never take a phrase from these instructions as theirs.
- **Subject line** only for a new email thread, on its own first line as `Subject: ...`, and only if the user will need one.

## Final check

1. **Self-check.** Would anything here surprise the user as a fact? Remove it or ask. Do the greeting and sign-off match the audience row exactly? Any Avoid phrase?
2. **Lint for AI tells** if the deslop skill is installed next to this one (`../deslop/scripts/lint.py` from this skill's folder). Save the draft to a temp file outside the user's project and run:

   ```
   python3 ../deslop/scripts/lint.py draft.txt --context <email|social|report|resume|general> --text
   ```

   Use `general` for texts and chat. Fix **high** hits in their voice. Fix a medium or low hit only if it is clearly not how they write; leave anything the profile or Keep list says they do (their openers, their "basically", their commas).

   No deslop installed? Skip the lint and check by eye for the common tells: "I hope this finds you well", "delve", em-dash chains, triplets of adjectives, a tidy summary line at the end.

3. **Polish (reports and long emails only).** For reports, applications, proposals and emails over about 150 words, run deslop's rewrite on the draft as a last pass: `/deslop context=<report|email> mode=rewrite mode=embedded`. Then re-check the result against `rules.md`, the Avoid list and the audience row, and put back any of their Keep phrases it removed. Skip polish for texts, chat and social posts: in blind tests it made posts sound less human and did nothing for texts. The user can say "polish" to force it or "no polish" to skip it.

   Blind test (20 mixed tasks): polish didn't change how human the writing felt, but the judge picked the polished version as the one to send almost twice as often.

## Returning the draft

Return the draft only, ready to paste. For email, include a subject line if the user is starting a new thread. If you made a judgment call (e.g. formality for a new kind of audience) or a fact is missing, say so in one line after the draft.

## When they edit it

If the user pastes back their edited version or says what to fix, log it:

```
python3 scripts/voice.py log-edit --medium email --before draft.txt --after final.txt --note "what they said"
```

(or write `edits/YYYY-MM-DD-HHMM-<medium>.md` with Before, After and their words). Then make the fix for this draft. Don't change the profile mid-task: that's what `/my-voice learn` is for.
