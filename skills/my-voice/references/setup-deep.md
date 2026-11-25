# Deep setup add-ons

Optional, in any order. Each one appends to the corpus, then rebuilds (references/builder.md) and shows test pieces. Same interview rules as quick setup.

## setup interview (30–40 min) → corpus/interview.md

The quick setup shows **how** they write. This shows **what they'd choose to say**: opinions, priorities, how they decide, what they stress to different people. One question at a time. Follow up once on anything vague ("What would you actually say to them?").

1. What's a strong opinion you hold about your field that most people get wrong?
2. Walk me through a recent decision you made at work. What did you weigh?
3. Explain your main project to (a) a customer, (b) an investor or boss, (c) a peer who does the same work.
4. What do you push back on most often, and how do you say it?
5. How do you deliver bad news?
6. How do you give critical feedback to someone you work with?
7. What do people misunderstand about you from your writing?
8. What do you never want to sound like?
9. What topics, details or worlds should never show up together? (Save the answers to `rules.md` too.)
10. Anything else a ghostwriter should know?

## setup scenarios+ (20–30 min) → corpus/scenarios-plus.md

Ten more scenarios, each with the incoming message shown and the constraint in bold. Tailor them to their world. Cover the mediums they use that `gaps.md` marks low:

1. Three resume bullets for their current or most recent role
2. A 2–3 sentence professional summary (resume or bio)
3. The opening paragraph of a monthly report or update
4. Critical feedback on a colleague's work
5. Saying no to a client who wants scope added for free
6. A long LinkedIn post announcing a launch
7. Asking someone senior for a favor or intro
8. A reply to an angry customer
9. A short thank-you after a meeting
10. A message to a close peer about something frustrating

## setup crosscheck (5 min)

A second model reviews the profile against the evidence. If the user has another model (e.g. GPT through Codex or an API), give it `profile/` plus `corpus/` with this prompt:

> Here is a writing-voice profile and the raw evidence it was built from. List every trait or rule in the profile that the evidence does not support, and every strong pattern in the evidence that the profile misses. Quote the evidence for each point. Be strict.

If no second model is available, run the same prompt in a fresh subagent. Save the output to `edits/YYYY-MM-DD-crosscheck.md`, show the user the findings, and apply only the ones they approve.

## setup blindtest (10 min)

See references/blindtest.md.

## setup samples

See references/samples.md.
