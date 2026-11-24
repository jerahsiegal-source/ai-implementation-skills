# Testing the skills

Each skill can have an `evals/` folder:

- `evals.json`: test prompts, each with what a good result looks like and a list of expectations to grade. It uses the same format as Anthropic's skill-creator, which OpenAI's Codex plugins also use.
- `trigger-evals.json` (for skills that start on their own): phrases that should and should not start the skill. Include near misses.
- `fixtures/`: the files the prompts refer to.

## How to run a test

1. **Run each prompt twice:** once with the skill, once without it (the baseline). In Claude Code the skill-creator skill can do this for you ("run the evals for the design skill"). In Codex, run the prompt in a project with the skill installed, then again with it disabled in `config.toml`.
2. **Run the page checker** on every page both runs made: `node skills/design-kit/scripts/check-page.mjs <page> --json`. This is the objective score: count of FAIL and WARN.
3. **Grade the expectations** for both runs. Each pass needs evidence (a screenshot, a line of checker output, a quote).
4. **Look at the screenshots side by side.** Design quality is judged by eye. Don't force it into pass or fail rules.
5. **Keep the result** if the skill clearly beats the baseline. If not, change the skill and test again.

Run the tests again when a new model comes out, in both Claude Code and Codex. A skill that no longer beats the baseline needs updating, or may no longer be needed.

## Checks on every push

`.github/workflows/checks.yml` runs the page checker's self-test on every push and pull request.
