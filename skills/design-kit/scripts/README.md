# Page checker

`check-page.mjs` catches AI slop and broken layout in an HTML page, so a skill can fix it before handing the page back. The design skills and the work loop run it on every page they make.

## Run it

From any skill folder:

```
node ../design-kit/scripts/check-page.mjs <page.html or url> --out <folder for screenshots>
```

| Option | What it does |
|---|---|
| `--out <dir>` | Where screenshots go. Default `./check-shots`. |
| `--json` | Print results as JSON (`summary` plus one entry per check). |
| `--allow id,id` | Accept patterns the user or brand asked for. The page can also say `<meta name="slop-ok" content="id,id">`. |
| `--static` | Skip the browser checks. |

Needs Node 18 or newer. The browser checks also need Playwright: `npm i -g playwright` then `npx playwright install chromium`. Without it they print `SKIP`, and the skill must say so.

## Reading the result

Each line starts with `FAIL`, `WARN`, `OK*` (allowed) or `SKIP`, then the check id. The last line counts them. Exit code `0` means no FAIL, `1` means at least one FAIL, `2` means the page could not be read.

**Loop rule:** fix every FAIL, judge every WARN, run again until the exit code is 0. Then look at the screenshots by eye with the [quality check](../quality-check.md). Never call a page done while it has a FAIL, or while browser checks were skipped without saying so.

## What it checks

**Look slop (from the page's CSS):** purple-to-blue gradient, cream plus terracotta palette, near-black with one neon accent, emoji as icons, a thick colored bar on every card, the same radius and shadow on every block, glass blur and glow, Inter as the only typeface.

**Word slop (from the visible text):** lorem ipsum, more than two em-dashes, "not X, but Y" framing, stock AI phrases, titles that read like descriptions, a page title with an explainer after a dash or colon, captions that repeat their heading, decorative 01 / 02 / 03 markers, several all-caps label styles, "→" on every link, "A · B · C" metadata lines.

**In the browser (Playwright):** screenshots at desktop (1280) and phone (390) in light and dark, sideways scroll on phone, text contrast (WCAG AA), text under 12px, mostly centered text, cut-off text, console errors, images without alt text.

These catch the common, objective problems. They cannot tell whether a design is good. That still needs the eye check, the swap test and a fresh critique.

## Test the checker

```
node test-check-page.mjs          # full test, needs Playwright
node test-check-page.mjs --static # without a browser
```

`fixtures/clean.html` must pass with no warnings, and `fixtures/slop.html` must trip every check. When you add a check, add its pattern to `slop.html` and its id to the test.
