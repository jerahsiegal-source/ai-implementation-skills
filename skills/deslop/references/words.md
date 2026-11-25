# Words

Single words are weak evidence. One "robust" in a page is fine; five stock words in one paragraph is a pattern. The linter starts word hits at **low** and raises them to **medium** when 3 land within about 120 words, and to **high** at 5. When you fix them, don't swap in a fancier synonym. Use the plain word, or cut it and say what actually happened.

The exact lists live in `scripts/rules.json`. Edit them there.

## W-01 Stock business verbs (low, clusters up)

spearheaded, leveraged, orchestrated, honed, streamlined, utilized, synergized, championed, fostered, empowered, facilitated, operationalized

These say "I was involved" without saying what you did. Replace with the real action (led, used, built, ran, cut, set up) and name the object.

> Before: Spearheaded and orchestrated a cross-team effort to streamline onboarding.
> After: Rewrote the onboarding checklist with HR and IT; new hires got laptops on day one instead of day four.

## W-02 Strong LLM vocabulary (medium)

delve, tapestry, realm, testament, multifaceted, ever-evolving, ever-changing, game-changer, at the forefront, embark on

These were rare in ordinary writing before 2023 and are common in model output. Use the plain word or drop the phrase.

> Before: Let's delve into the multifaceted realm of pricing.
> After: Pricing has three parts: list price, discounts and contract length.

## W-03 Common LLM vocabulary (low, clusters up)

intricate, showcasing, pivotal, underscore, nuanced, robust, seamless, holistic, paramount, vibrant, bustling, meticulous, unlock, unleash, elevate, harness, cutting-edge, comprehensive, crucial, invaluable, meaningful, impactful, resonate

Ordinary words that models overuse. Leave one alone if it is the right word ("robust routing" in a framework README is fine). Fix them when they cluster.

> Before: A robust, seamless and comprehensive platform that elevates your workflow.
> After: It syncs your calendar and task list every five minutes.

## W-04 Figurative landscape / navigate (medium)

"the competitive landscape", "the digital landscape", "navigate the complexities of", "navigate the challenges"

Literal landscapes and literal navigation are fine. The figurative use hides the actual market or problem.

> Before: Navigating the complexities of today's regulatory landscape.
> After: Meeting the new EU data rules that take effect in March.

## W-05 Transition used as an opener (low, clusters up)

Moreover, Furthermore, Additionally, Notably, Importantly, In essence, Crucially, Interestingly

Delete the word; the sentence nearly always works without it. "Ultimately" is treated as a summary closer (P-04).

> Before: Additionally, the team shipped the export feature.
> After: The team also shipped the export feature.

## W-06 Resume and cover-letter cliches (medium; high in resume)

results-driven, detail-oriented, team player, proven track record, passionate about, excellent communicator, self-starter, dynamic professional, highly motivated, valuable addition, aligns perfectly with, eager to contribute, make a real difference

Every applicant writes these, so they carry no information. Cut them or replace with one piece of evidence.

> Before: Results-driven, detail-oriented marketer with a proven track record.
> After: Marketer who grew a newsletter from 8,000 to 21,000 subscribers in two years.

## W-07 Empty intensifiers (low, clusters up)

truly, deeply, incredibly, highly, extremely, remarkably, profoundly, undeniably, absolutely

They add emphasis, not information. Cut them. If the point needs weight, add a fact.

> Before: We are truly, deeply grateful for an incredibly successful year.
> After: Thank you. Revenue grew 18% this year.

## W-08 Size word with no number (medium)

significantly, substantially, dramatically, drastically, vastly, exponentially, massively, greatly

Flagged only when the same sentence has no number. Give the number, or mark the gap. Never make one up.

> Before: The redesign significantly improved conversion.
> After: The redesign improved conversion [NEEDS SPECIFIC: from what rate to what rate?].
