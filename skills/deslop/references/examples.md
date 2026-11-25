# Examples

One before/after pair per context. Each "after" keeps every fact from the "before", adds none, and marks what's missing.

## resume

Before:
```text
Results-driven Marketing Manager with a proven track record of driving growth.
- Spearheaded email campaigns in HubSpot, resulting in increased engagement.
- Leveraged data-driven insights to optimize open rates.
- Grew the newsletter list from 8,000 to 21,000 subscribers.
- Partnered with cross-functional teams to align initiatives with business goals.
```

After:
```text
Marketing manager who grew a retail newsletter from 8,000 to 21,000 subscribers.
- Ran email campaigns in HubSpot [NEEDS SPECIFIC: how many per month, and what changed in engagement?].
- Tested subject lines and send times to raise open rates [NEEDS SPECIFIC: from what to what?].
- Grew the newsletter list from 8,000 to 21,000 subscribers.
- Planned launches with sales, design and e-commerce.
```

Changes: removed 2 cliches (results-driven, proven track record), 2 stock verbs (spearheaded, leveraged), 2 vague impact phrases; broke the "resulting in" pattern; added 2 markers.

## report

Before:
```text
In this report, we'll explore the results of our four-day week pilot. The pilot played a pivotal role in our wellness strategy. Sick days fell from 61 to 38, and 41 of 46 participants asked to keep it. Overall, these results underscore our commitment to our people.
```

After:
```text
The four-day week pilot worked: sick days fell from 61 to 38, and 41 of 46 participants asked to keep it.
```

Changes: cut section narration, inflated significance and the summary closer; moved the conclusion to the first line.

## email

Before:
```text
Hi Dana,

I hope this email finds you well! I wanted to reach out to provide a quick update regarding the analytics dashboard. Unfortunately, due to unforeseen circumstances related to data warehouse access, the timeline will need to be adjusted.

**New date:** one week later than planned.

Please don't hesitate to let me know if you have any questions!
```

After:
```text
Hi Dana,

The analytics dashboard will be a week late. Our data warehouse access came through late [NEEDS SPECIFIC: on what date?], so the new delivery date is [NEEDS SPECIFIC: exact date].

Let me know if you have questions.
```

Changes: cut the opener and over-explanation, removed markdown bold and exclamation marks, added 2 markers.

## social

Before:
```text
Excited to share that I just launched my first open-source project! 🚀

It's not just a CSV cleaner. It's a time-saver.

The result? Hours back in your week.

#opensource #CLI #Python #DataCleaning #BuildInPublic
```

After:
```text
I just released my first open-source project: a command-line tool that fixes inconsistent headers, stray whitespace, duplicate rows and broken encodings in CSV files [NEEDS SPECIFIC: name and link?].

If you clean CSVs by hand before every analysis, try it and tell me what's missing.

#opensource #Python
```

Changes: cut the announcement opener, emoji, contrast frame and Q-and-A reveal; cut 3 hashtags; added 1 marker.

## docs

Before:
````text
## Why tidycsv?

tidycsv is a blazing-fast, robust and seamless solution that empowers you to unlock the full potential of your data.

```bash
pip install tidycsv
```
````

After:
````text
## Why tidycsv?

tidycsv fixes headers, whitespace, duplicate rows and encodings in CSV files with one command [NEEDS SPECIFIC: speed on a typical file, if you want to claim it?].

```bash
pip install tidycsv
```
````

Changes: cut 3 LLM words and 2 hype phrases; code block untouched.

## web

Before:
```text
Revolutionize your restaurant's finances with LedgerLine's world-class, seamless bookkeeping. We empower owners to unlock actionable insights and drive results.
```

After:
```text
LedgerLine does the books for restaurants: daily reconciliations, tip reporting, payroll and monthly reports [NEEDS SPECIFIC: price, or who it's for, e.g. single location vs groups?].
```

Changes: cut 2 hype words, 1 LLM word, 2 vague impact phrases; replaced the claim with what the service does, using only facts from the source page.

## general (already clean: leave it)

Before and after:
```text
Every two weeks, a new cohort joins our team. Members of the cohort may live in different places, and have different skillsets, backgrounds, and learning styles.
```

Output: `Already clean. 0 changes.` A list of three that is a real list is not a tell, and a human sentence doesn't need a marker.
