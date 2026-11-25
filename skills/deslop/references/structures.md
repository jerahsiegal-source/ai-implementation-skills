# Structures

Sentence and paragraph shapes outlast vocabulary. Each new model drops some of the old words, but the shapes stay. The linter catches the regular ones; S-07 needs your judgment.

## S-01 Rule of three (low; medium when it repeats)

Lists of three adjectives, nouns or clauses, used out of habit. The linter counts lowercase "X, Y, and Z" lists of similar length and raises them to medium at 4 or more per 500 words. Lists of names, numbers or genuinely three things are fine; humans write those all the time.

> Before: A fast, secure, and reliable platform for modern, agile, and growing teams.
> After: A platform that stays up during your release-day traffic.

Fix: keep the one or two items that matter, or make the list a real list.

## S-02 Negation / contrast frame (medium; high in social)

"It's not X, it's Y." "Not just X but Y." "X isn't about A. It's about B." "Not because X, but because Y." "It's less about X and more about Y."

It invents an opposing view just to knock it down. State Y directly.

> Before: It's not just a CRM, it's a growth engine.
> After: It tracks every deal and reminds reps to follow up after three days of silence.

## S-03 Binary framing (medium)

"On one hand... on the other hand." Fine in a real trade-off analysis; a tell when the text never picks a side. Say which side you land on, or list the trade-off plainly.

> Before: On one hand, remote work offers flexibility. On the other hand, it presents challenges.
> After: Remote work saved our team 6 hours of commuting a week and made onboarding slower.

## S-04 Uniform rhythm (medium; low in resume and docs)

Sentences of nearly the same length, one after another. The linter flags a low coefficient of variation (under 0.30 across 6+ sentences) or 5 sentences in a row within 3 words of each other. Fix by joining two short sentences, splitting a long one, and letting one be very short.

> Before: The team launched the feature in May. Users adopted it quickly across regions. Support tickets declined over the next month. Leadership approved further investment in June.
> After: The team launched the feature in May. Within a month, support tickets about exports fell by a third, and in June leadership funded the next phase. That was fast.

## S-05 Same-shape bullets (medium; high in resume)

Every bullet starts the same way: the same word, or a past-tense power verb every time (Spearheaded, Leveraged, Orchestrated...), or verb + vague object + "resulting in". In a resume, action verbs are normal; the flag is 3+ stock verbs in a row.

> Before:
> - Spearheaded the migration, resulting in improved performance.
> - Leveraged analytics, resulting in better decisions.
> - Orchestrated launches, resulting in increased adoption.
>
> After:
> - Moved 40 services from Heroku to AWS ECS; p95 latency fell from 900 ms to 300 ms.
> - Weekly funnel report now decides which onboarding step gets fixed next.
> - Ran 6 launches with marketing; the March one reached 12,000 users in two weeks.

## S-06 "resulting in" tail (low; medium when repeated in a list)

", resulting in...", ", leading to...", "which resulted in..." bolted onto the end of a sentence to suggest impact. Give the result as its own fact, or mark it with `[NEEDS SPECIFIC]`.

## S-07 Paragraph template (judgment, not linted)

Topic sentence, three supporting points, summary sentence, repeated paragraph after paragraph. Look for it when several paragraphs have the same internal movement. Fix by cutting the summary sentences and letting paragraph length follow the content.

## S-08 Summary sentence ends the paragraph (medium; high in report)

The last sentence starts with "Overall", "Ultimately", "This shows", "These results suggest"... and restates the paragraph. Cut it.

> Before: Tickets fell 20% and response time halved. Overall, these results demonstrate the team's commitment to excellence.
> After: Tickets fell 20% and response time halved.

## S-09 Section narration (medium; high in report)

"In this section, we'll explore...", "Let's take a look at...", "We'll dive into...", "Without further ado". The document describes itself instead of its subject. Delete the sentence and start with the content.

## S-10 Rhetorical question, then answer (medium; high in social)

"The result? Faster deploys." "So why does this matter? Because..." Write it as a statement.

> Before: The result? A 40% drop in churn.
> After: Churn fell 40%.

## S-11 Colon reveal and punchy fragments (medium; high in social)

"Here's why:", "Here's the kicker:", or a dramatic fragment used as a habit ("Simple." "Full stop." "Let that sink in."). One on purpose is style; one per paragraph is a tic.

## S-12 False agency (low)

Abstractions doing human things: "the data tells a story", "the market rewards", "the decision emerged". Name who did it.

> Before: The data tells us customers want faster shipping.
> After: In our March survey, 61% of customers ranked shipping speed first.

## S-13 One-line paragraph drama (medium; high in social, social only)

Four or more one-sentence paragraphs in a row, each short, for suspense. Join them into real paragraphs.

## S-14 First person in a resume (medium, resume only)

Resumes drop "I" and "my". Start bullets with the verb.

## S-15 Negative listing (medium)

"Not a tool. Not a platform. A partner." Listing what something isn't before saying what it is. Say what it is.
