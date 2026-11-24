# Floor: rules that hold in every style

Every style, brand and personal preference sits on top of these. A brand or a user request can change how things look, but it never removes these.

## Rule order

When instructions disagree, the higher one wins:

1. What the user says in this conversation
2. The project's `DESIGN.md` and brand guide
3. Personal taste in `~/.ai-skills/personal/` (if it exists)
4. This kit's generic defaults and styles
5. General design conventions

The floor below sits under all five: accessibility, working features and honest data are never traded away for looks. If a user request would break the floor, do it their way only after saying in one line what it costs.

## Readability

- Body text 16px or larger (17 to 18px for long reading). Line height about 1.5.
- Lines of running text at most about 70 characters.
- Left-aligned text. No justified paragraphs. No long runs of all caps or italics.
- Clear sans-serif for body text unless the brand says otherwise. Use real font fallbacks. Avoid fonts with a slashed or dotted zero in reading text (it reads as 8 or Ø); keep those for code and IDs.
- One idea per short paragraph. Use headings, lists and visuals before long prose.
- Contrast at least WCAG AA (4.5:1 for body text, 3:1 for large text and UI parts).

## Accessibility

- Never use color alone to show meaning. Pair it with an icon, a word or a shape (for example ✓ Done, ! Blocked).
- Every interactive element works with the keyboard and has a visible focus state.
- Tap targets at least 40px. Labels on every form field.
- Respect `prefers-reduced-motion`. Motion explains something or it goes.
- Works at phone width (about 400px) with no sideways page scroll.

## Honest data

- Chart scales start where they should (bars at zero), and labels match real values.
- Show the source or date for any number that came from somewhere.
- Do not round, crop or color data to make it look better than it is.
- Use example data only when it is clearly labeled as example data.

## Working features

- Redesigns keep every existing feature and data field unless the user says to drop it.
- Design every state that matters: empty, loading, error, success, hover, focus, disabled.

## Copy

- Short, plain, specific. Name things the way users know them, not how the code names them.
- Buttons say what happens ("Run test", not "Submit").
- **No personal data in URLs.** Names, emails and anything the user typed never go in a link or query string; neither do passwords or tokens.
- **No false promises.** Never say something happened or will happen ("Check your inbox", "Ready in 2 minutes", "3 of 3 done") unless the product actually does it. If it is a mockup, label it as one.
- No filler intros, no marketing fluff on internal tools, no lorem ipsum.
- **Titles are names, not descriptions.** A page or section title is 1 to 6 words ("Visualize, round three", "Decisions"). The verdict or one-line summary goes below it, set smaller.
- **One line or nothing.** Subtitles, captions and card blurbs are one short line. If a caption repeats the title or the obvious, delete it.
- **Cut AI tells in copy:**
  - sentences that explain the page itself ("Every page below is…") or restate the heading
  - colon reveals in titles ("Mission Map: the system as a graph") and "not X, but Y" framing
  - "X, Y, and Z" triplets, em-dashes, and words like seamless, robust, comprehensive, elevate, unlock
  - ALL-CAPS eyebrow labels stacked above every title; use sentence case, and only where the label adds facts (a date, a count)
  - an arrow on every link; keep it for the one main action

## Anti-slop: avoid these unless asked

These looks scream "an AI made this". Use one only when the user or brand asks for it.

- Purple-to-blue gradient hero on white
- Cream background with a serif headline and a terracotta accent
- Near-black with a single neon green or orange accent
- Emoji as section icons
- Everything centered, everything a rounded card with the same shadow
- Colored accent bar down the side of every card
- Three identical feature cards under a giant hero, by default
- Numbered 01 / 02 / 03 markers on things that are not a sequence
- Long sentence-style headlines and a caption under every element
- Decorative blobs, glassmorphism and glow for no reason
