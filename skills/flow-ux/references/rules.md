# Flow rules

Rules for building flows, forms and navigation well the first time. `/design` reads this file when the job has a multi-step flow, a form or navigation. `/flow-ux` reviews against the same rules.

## Flows

- **One job per screen.** Each step has one clear goal and one primary button.
- **Fewest steps, then fewest decisions.** Remove a step before you polish it. Ask only what you need now; ask the rest later or infer it.
- **Show where they are** in flows of 3 or more steps: "Step 2 of 4" with names, not dots alone.
- **Never lose work.** Keep input through errors, back, refresh and sign-in. Save drafts on long forms.
- **Always a way out:** back, cancel or undo on every step. Confirm only actions that can't be undone, and say what will be lost.
- **End on a clear result:** what happened, what's next, and the one button to do it. Only claim what really happened.
- **Edit returns you.** Editing a step from a summary brings you back to the summary.
- **Never store secrets in the browser** (passwords, tokens, card numbers) or put them in URLs.

## Forms

- **One column.** Labels above fields, always visible (not placeholder-only).
- **Mark the exception.** If most fields are required, mark the optional ones, and vice versa.
- **Right input, right keyboard:** `type="email"`, `tel`, `inputmode="numeric"`, `autocomplete` on every common field.
- **Smart defaults** and the most common choice preselected when it is safe.
- **Errors never move the button they're about to press.** Reserve space for messages, or validate on submit, so a blur error can't push Continue out from under the click.
- **Validate when they leave a field, not on every keystroke.** Errors sit next to the field, say what to change ("Use 8 or more characters"), and don't wipe the input.
- **Buttons say what happens:** "Create account", not "Submit". The primary button stays enabled and explains what's missing if pressed early.
- **Group** long forms into short titled sections. Advanced options behind a toggle.

## Navigation

- **Their words** for menu labels, not internal names.
- **Five to seven top-level items** at most. Current place always highlighted.
- **Same place, same thing:** navigation doesn't move or change between screens.
- **Search** when there are more than a couple dozen destinations.
- **Phone:** the main destinations reachable with a thumb; no hover-only menus.

## Feedback

- Respond to every action within about 100ms (pressed state), show progress after about 1 second, and give a time or a step count for anything over 10.
- Success is confirmed where the person is looking, not only in a toast that vanishes.
- Empty states say what goes here and offer the action that fills it.
