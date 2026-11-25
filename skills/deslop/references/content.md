# Content

This is the highest-value pass, and no regex can do it. Text with every surface tell removed but nothing specific inside is still bad writing; it is just harder to spot. Hiring managers and readers reject vagueness, not AI involvement. So read each sentence and ask: does it tell the reader something they could check, or something only this author could say?

The one hard rule: **never invent a fact.** When a sentence needs a detail you don't have, insert a visible marker and move on:

`[NEEDS SPECIFIC: how much faster?]`

Keep the question short and concrete: a number, a tool, a name, a "for whom", a "compared with what". Every marker goes in the NEEDS YOUR INPUT list.

## C-01 Unanchored claims (high)

"Improved efficiency." "Enhanced the customer experience." "Streamlined operations." Ask what changed, by how much, for whom, and how. If the text or the conversation gives the answer, use it. If not, mark it.

> Before: Improved reporting efficiency for the finance team.
> After: Automated the month-end revenue report for the finance team [NEEDS SPECIFIC: hours saved per month?].

## C-02 Interchangeable sentences (medium)

If a sentence could appear unchanged in anyone's resume or any company's report, it says nothing about this one. Replace it with something specific from the text, or cut it. Don't add a marker to every one; cut the ones that carry no claim at all.

> Before: We are committed to delivering exceptional service to our valued customers.
> After: (cut; or, if the text has it: "Every order ships within 24 hours.")

## C-03 Inflated importance (medium)

A minor fact dressed as a milestone: a routine update "marks a new chapter", a small feature "revolutionizes" a workflow. Describe it at its real size.

## C-04 Restating (medium)

A sentence or paragraph that repeats what was just said in different words, often as a closer. Cut the repeat.

## C-05 Over-politeness and over-explanation (low)

Justifying things nobody asked about, pre-apologizing, thanking at length, explaining what the reader already knows. Trust the reader. Delete the justification.

> Before: I wanted to reach out to provide a quick update, as I understand how important it is to keep you informed about the timeline.
> After: Quick update on the timeline.

## C-06 Invented-looking precision (medium; flag, don't remove)

Round numbers or percentages with no source in a context that needs one ("studies show 73% of customers..."). You can't tell if it is real. Don't delete it and don't change it; add a marker after it: `[NEEDS SPECIFIC: source for 73%?]`. In a resume, the author's own numbers don't need a source.

## C-07 Stiff phrasing (medium)

Sentences that are grammatical and free of obvious tells but still sound like a form or a press release: "We appreciate your patience as we work to resolve this", "Please do not hesitate to reach out", "This initiative was designed to test whether", "in order to ensure alignment". A person would say it shorter and in everyday words. Rewrite it the way you would say it to the reader across a table, keeping every fact. This is the fix that makes text read as human; deleting flagged words alone leaves it stiff.

> Before: This initiative was designed to test whether a compressed schedule could enhance work-life balance without compromising output.
> After: We wanted to know if people could work four days without getting less done.

Use it only when the linter score is below 85, the user says the text is AI-written, or `mode=rewrite` is set, and only on sentences that read like a form. Never apply it to text that sounds like a person: jokes, asides, opinions, enthusiasm and odd specific details ("Go Sooners!", "ancient forests") are voice, not stiffness. Legal and regulatory wording stays too.

## How many markers

Markers are for claims that matter. A human-written text that is already specific should get zero or one. If you are about to add more than one marker per 100 words, you are probably flagging style, not missing facts; keep the most important ones and cut or simplify the rest of the vague sentences instead.
