# Heuristics and severity

Sweep the whole flow with these after the step-by-step questions. Each is a lens, not a box to tick: report only what you saw happen.

## Severity (0 to 4)

Rate by three things together: how many people hit it, whether they can get past it, and whether it happens every time.

| | Meaning | Example |
|---|---|---|
| **4** Blocker | The person cannot finish, loses data or money, or is told it worked when it didn't | Submit does nothing on phone; form clears on error |
| **3** Major | They finish only after real confusion, a retry or help, or an accessibility failure blocks some people | Error says "Invalid input" with no hint what to change; fields labelled only by placeholders |
| **2** Minor | Slows them down or makes them hesitate | Required fields not marked until submit |
| **1** Cosmetic | Noticeable, doesn't slow anyone | Inconsistent button casing |
| **0** Not a problem | Drop it | |

Based on Jakob Nielsen's severity ratings.

## Ten heuristics

Jakob Nielsen's ten usability heuristics, phrased as questions.

1. **Status:** does the person always know what's happening (loading, saving, step 2 of 4)?
2. **Their words:** do labels match how they talk, not how the code or the company talks?
3. **Way out:** can they go back, cancel or undo without losing work?
4. **Consistency:** do the same things look and behave the same, and follow platform conventions?
5. **Prevent errors:** do defaults, constraints and confirmations stop mistakes before they happen?
6. **Show, don't make them remember:** is what they need on screen, not something to carry over from an earlier step?
7. **Fast paths:** can returning users skip ahead (autofill, saved choices, shortcuts)?
8. **Only what matters:** does each screen hold only what this step needs?
9. **Recover from errors:** does every error say what went wrong and how to fix it, next to the problem?
10. **Help in place:** is help where the question comes up, not on a separate page?

## Also check

- **Accessibility** (WCAG 2.2): everything works by keyboard in a sensible order with a visible focus; focus is never hidden under sticky bars; tap targets are at least 24 by 24px (44 is better on phone); errors are announced, not shown by color alone; sign-in doesn't require solving a puzzle or retyping a code from memory; nothing asks for the same information twice.
- **Choices:** more options mean slower decisions (Hick's law). Recommend one, hide the rest behind "more".
- **Reach:** the main action is big and near where the eye or thumb ends (Fitts's law).
- **States:** empty, loading, slow, error, success and partial states are all designed.
