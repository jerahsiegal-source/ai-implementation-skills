# Flow UX

Can a real person finish the task? Flow UX walks through your sign-up, checkout, setup or form like a user would, then ranks what gets in the way, with a screenshot for each problem.

Type `/flow-ux` (Claude Code) or `$flow-ux` (Codex):

```
/flow-ux Can a first-time user create and send an invoice?
/flow-ux Review the sign-up on localhost:3000
/flow-ux fix the onboarding flow
```

## How it works

1. **Frame:** who the person is, the task, and what "done" looks like
2. **Walk it:** the happy path, a mistake path, keyboard only, and on phone, with a screenshot of every step
3. **Four questions at every step:** will they try the right thing, see how, know it's the right control, and know it worked?
4. **Rank:** every problem gets a severity from 4 (blocks the task) to 1 (cosmetic), the step it happens on, and the smallest fix
5. **Report:** a visual map of the flow with problems pinned to each step (with [visualize](../visualize)), or a short markdown report
6. **Fix (on request):** fixes the worst problems first, walks the flow again, and stops when nothing major is left

`/design` also borrows Flow UX's [rules](references/rules.md) when it builds forms, multi-step flows or navigation.

Uses the shared [design kit](../design-kit) and its page checker. Install with the repo's install script.

---
Built by [Jerah Siegal](https://www.linkedin.com/in/jerah-siegal-ai-tech/) · MIT License
