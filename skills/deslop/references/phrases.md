# Phrases

Stock phrases are stronger evidence than single words, because a writer has to choose the whole phrase. Most of them can simply be deleted.

## P-01 Throat-clearing opener (medium; high in email and social)

"In today's fast-paced world", "In the ever-evolving landscape of", "When it comes to", "It's worth noting that", "It's important to note that", "Let's dive in", "Here's the thing", "It goes without saying", "At the end of the day", "In a world where"

They delay the point. Cut the phrase and start with what it was introducing.

> Before: When it comes to onboarding, it's important to note that first impressions matter.
> After: New hires decide in the first week whether the job matches the offer.

## P-02 Chatbot leftovers (high)

"Great question", "I hope this helps", "Certainly!", "As an AI", "Let me know if you'd like", "Here's a breakdown of", "I'd be happy to help", "Would you like me to", "Hey there!", "I hope this email finds you well"

These are replies to a chat, pasted into a document. Delete them. (A plain "let me know if you have questions" at the end of a real email is fine; humans wrote that before chatbots.)

> Before: Certainly! Here's a breakdown of the Q3 numbers. I hope this helps!
> After: Q3 numbers:

## P-03 Inflated significance (medium; high in report)

"plays a vital/pivotal/crucial role", "stands as a testament to", "a pivotal moment", "marks a significant shift", "rich cultural heritage", "enduring legacy", "a broader movement", "cannot be overstated", "nestled in", "paradigm shift"

The sentence tells the reader how much something matters instead of showing it. Say what happened and let the reader judge.

> Before: The new warehouse plays a pivotal role in our growth and marks a significant shift in strategy.
> After: The new warehouse in Reno cuts West Coast delivery from five days to two.

## P-04 Summary closer (medium; high in report)

"In conclusion,", "In summary,", "Overall,", "Ultimately,", "To sum up,", "All in all,", "In short,", "At its core,"

A wrap-up that repeats what the reader just read. Cut it. In a report, put the conclusion first instead of last.

> Before: Overall, the quarter showed strong progress across all key areas.
> After: (delete; the numbers above already say this)

## P-05 Hedge stack (medium)

Two or more hedges on one claim within a few words: "may potentially", "could possibly help to somewhat", "might arguably", "generally tends to".

One hedge is honest. A stack is noise. Keep one, or none if you know it's true.

> Before: This change may potentially help to somewhat reduce churn.
> After: This change may reduce churn.

## P-06 Vague impact phrase (medium; high in resume and web)

"drive results", "deliver value", "make an impact", "data-driven insights", "cross-functional initiatives", "optimize workflows", "actionable insights", "best-in-class", "move the needle", "key stakeholders", "improved efficiency", "enhanced collaboration"

Each one points at a result without stating it. Name the result (what changed, by how much, for whom) or mark it with `[NEEDS SPECIFIC: ...]`.

> Before: Delivered actionable insights that drove results for key stakeholders.
> After: Built the weekly churn report the CFO uses to set renewal discounts.

## P-07 Hype word (low; high in web, social and docs)

revolutionize, transformative, next-level, world-class, unparalleled, unmatched, supercharge, state-of-the-art, effortless, blazing fast, unlock the full potential, a bold step

Claims the reader can't check. Replace with what the product does and a fact they can verify.

> Before: Supercharge your workflow with our revolutionary, world-class editor.
> After: The editor opens a 200 MB log file in under a second.

## P-08 Point-announcing scaffold (low)

"The key is", "This matters because", "The bottom line is", "What's interesting is", "The reality is", "Make no mistake", "The good news is", "Key takeaways include"

A drum roll before the point. Drop the announcement and say the point.

> Before: The bottom line is that the pilot worked.
> After: The pilot worked: sick days fell from 61 to 38.

## P-09 Announcement opener (medium)

"Excited to share", "Thrilled to announce", "I am thrilled to submit", "Proud to be", "Humbled to"

The standard first line of generated posts and cover letters. Start with the news.

> Before: Thrilled to share that I just launched my first open-source project!
> After: I just released tidycsv, a command-line tool that fixes broken CSV headers and encodings.

## P-10 Unfilled placeholder (high)

"[Your Name]", "[X%]", "[metric]", "[Company]", "[N] users"

A template slot nobody filled. Convert it to a `[NEEDS SPECIFIC: ...]` marker so it lands in the needs-input list and can't ship by accident. Never fill it with a guess.

> Before: Grew [metric] by [X%] year over year.
> After: Grew [NEEDS SPECIFIC: which metric?] by [NEEDS SPECIFIC: how much?] year over year.
