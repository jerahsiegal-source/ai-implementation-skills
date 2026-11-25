# Quick setup (about 25 minutes)

Run `python3 scripts/voice.py init` first. Open with one sentence: 5 steps, about 25 minutes, answers saved word for word, dictation is fine. If the session has a task list, add the 5 steps and tick them off.

Follow the interview rules in SKILL.md. Append each answer to its file as soon as it arrives, under a `## Prompt` / `## Q` / `## Scenario` / `## Round` heading that names the question.

---

## Step 1: Talk (5 min) → corpus/talk.md

Ask one at a time:

1. Explain what you do to a friend who works outside your field.
2. Tell me about something you built or fixed recently.

These show vocabulary and how they explain things. Dictated answers show speech, not punctuation.

**Use what they say here to tailor steps 3 and 4** to their real job, people and tools.

## Step 2: Habits (3 min) → corpus/habits.md

One at a time:

1. How do you usually open and close your messages?
2. Are there any words or phrases you'd never use?
3. What annoys you in other people's writing?
4. How does your writing change when it's going to a boss versus a peer?
5. Do you use emoji? If so, where?
6. Do you tend to write short messages or long ones?

If they mention hard rules (e.g. "I never mix my day job into my business emails"), also add them to `rules.md`.

## Step 3: Scenarios (12 min) → corpus/scenarios.md

Six situations. For each one, **show the incoming message**, written for their world, using names and details that fit what they said in Step 1. Put the constraint **in bold**. Ask them to write the exact message they'd send.

| # | Situation | Constraint to bold |
|---|---|---|
| 1 | Decline or push back on a request (from a colleague or client) | They can't meet the deadline |
| 2 | Update their boss on a delay | It won't be done on time, and the real reason (give one) |
| 3 | Follow up with no reply (show the email they sent 8 days ago) | No reply yet |
| 4 | Cold outreach to a stranger who could use their work | They've never met; one thing they know about the person |
| 5 | Explain something technical to a non-technical person who asked "keep it simple" | The real cause and fix (give them) |
| 6 | Short public post (LinkedIn, X, etc.) about something they did | What they did (use something real from Step 1) |

Format each prompt like this:

> **From:** [Name] ([role])
> **Subject:** [subject]
>
> [2–4 line body]

**The situation:** [constraint, in bold]. Write your reply.

Save the incoming message (or a one-line summary of it) above their answer.

## Step 4: Taste test (4 min) → corpus/taste.md

Eight A/B rounds. One style choice per round, with short options set in their world. Reason optional; save it word for word. Defaults (adapt the content):

1. Warm-up opener vs straight to the point
2. Hedged claim ("I think we could probably...") vs confident claim
3. Clean vs profane (an internal note to a coworker)
4. One-thought paragraphs vs bullets (a short status email)
5. Precise numbers vs vague timing
6. Calendar link vs proposing specific times
7. Punchy hook vs soft opener (a public post)
8. Apology with an exclamation mark vs a plain apology

If they say "neither" and write their own version, that's the best answer you'll get. Save it.

## Step 5: Build + check (2 min) → profile/

Follow references/builder.md. Then show 2 short test pieces in different mediums and ask for "sounds like me" or "fix X" on each. Save the verdict to `edits/YYYY-MM-DD-setup-check.md`.

Then offer the most useful next step. It's almost always **samples**: real writing beats everything else.
