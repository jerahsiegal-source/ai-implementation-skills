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
- Clear sans-serif for body text unless the brand says otherwise. Use real font fallbacks.
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
- No filler intros, no marketing fluff on internal tools, no lorem ipsum.

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
- Decorative blobs, glassmorphism and glow for no reason
