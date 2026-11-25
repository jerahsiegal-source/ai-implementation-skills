# Formatting

Formatting tells are easy to fix and easy to over-fix. Change the formatting, never the facts inside it.

## F-01 Em dashes (low; medium when frequent)

Default policy: replace em dashes with a comma, period, colon or parentheses. The linter flags each one and raises them to medium above 2 per 300 words. Pass `--allow-em-dash` (or say "keep em dashes") when the author uses them on purpose; many human writers do. The real tell isn't the character, it's the formulaic use: a dash before a punchline, in every sentence.

> Before: We shipped it — and it changed everything.
> After: We shipped it in May, and support tickets dropped by half.

Never change dashes inside code, URLs, quotes, or ranges like "2019–2022".

## F-02 Mixed quote styles (low)

Curly quotes (“ ” ‘ ’) and straight quotes (" ') in the same text often means model output was pasted into hand-written text. Pick one style and use it throughout. Never change quotes inside code.

## F-03 Emoji (medium; high in email, social, and as bullets anywhere)

Emoji in professional text, and especially emoji used as bullets or heading icons (🚀, ✅, 🔹, 📈). Remove them. In a casual social post one emoji can stay if the author clearly chose it.

> Before: 🚀 **Lesson 1: Communication is everything.**
> After: The first lesson was about communication.

## F-04 Bold mid-sentence (low; medium at 4+)

Bolding phrases inside sentences for emphasis, many times. Bold one thing at most, or none. (Bold labels at the start of a bullet are F-07.)

## F-05 Title Case Headings (low; off in resume, report, docs, web)

Every heading In Title Case Like This. Use sentence case unless a style guide says otherwise.

## F-06 Too many headings (low)

Three or more headings in a text under 600 words with less than 60 words per heading. Short text rarely needs headings. Cut most of them.

## F-07 "Label: explanation" bullets (medium; low in resume, report, docs)

Every bullet starts with a bolded label and a colon:

> - **Speed:** Our tool is fast.
> - **Security:** Your data is safe.
> - **Support:** We're here to help.

Turn them into plain sentences, or a real table if it is reference material. A single labelled list in a report is fine; every list in the document labelled this way is the tell.

## F-08 Markdown in plain text (high, email only)

`**bold**`, `### headings`, `- [ ]` checkboxes or tables in an email or other plain-text destination. They show up as literal symbols. Remove them and use plain line breaks.

## F-09 Hashtag wall (medium; high in social)

Four or more hashtags, usually stacked at the end. Keep two or three that people actually search, or none.

## F-10 Exclamation marks in professional text (low; medium at 2+)

Off in social. Cut them; let the facts carry the energy.

## F-11 Long title or subtitle (medium)

A heading over 8 words, a "Title: subtitle" heading, or an italic subtitle line under the title. People write short titles: "Q3 support report", not "Q3 Support Report: Driving Customer Satisfaction Through Faster Resolution". Keep the noun, cut the pitch, and drop the subtitle line.

> Before: ## Building Resilience: How Our Team Navigated a Challenging Quarter
> After: ## Q3 recap

