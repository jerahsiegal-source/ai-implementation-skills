# Quality check

Run this before handing any visual work back. Inside a work loop, the screenshots and this list are the evidence for every design item.

## How

1. **Automated checks first.** If [`scripts/check-page.mjs`](scripts/) is present, run it on the page or URL from the skill folder:
   `node ../design-kit/scripts/check-page.mjs <page.html|url> --out <dir>`
   Fix every `FAIL`, judge every `WARN`, and re-run until it exits 0. Accept a pattern only when the user or brand asked for it (`--allow <id>`). Show the summary line and every `SKIP`. Never call a page done with a `FAIL`, or with render checks skipped without saying so.
2. Render the real thing: open the page, run the app, or open the HTML file in a browser (Playwright or the tool's browser).
3. Screenshot at desktop width (about 1280px) and phone width (about 400px), or use the ones the script saved. If the page has dark mode, check both themes. Look at every screenshot yourself.
4. Go through the list below. Then **critique** like a strong studio would: name the weakest part of the page and the most generic-looking part.
5. **Fix, then re-run steps 1 to 4.** Outside a work loop, stop after two rounds and report what is left. Inside a work loop, each round is one attempt on the item, under the loop's stop rules.

## The list

- [ ] **5-second test:** the most important thing on screen is obvious without reading.
- [ ] **One focal point** per view. Nothing else competes with it.
- [ ] **Hierarchy:** headings, numbers and actions are clearly ranked by size, weight and position.
- [ ] **Floor:** readable text, contrast, icon plus word for status, focus states ([floor.md](floor.md)).
- [ ] **Fits the surface:** density and layout match the surface notes (busy dashboard is fine, busy landing page is not).
- [ ] **Brand and style:** colors, type and tokens come from `DESIGN.md` or the chosen style, not random values.
- [ ] **Craft:** type scale, spacing scale, alignment and one accent hold up ([craft.md](craft.md)), and the polish pass is done.
- [ ] **Would ship:** a strong studio would put its name on this. If not, name the weakest part and fix it.
- [ ] **Short copy:** every title is a name of 6 words or fewer; every caption is one line or gone ([floor.md](floor.md#copy)).
- [ ] **Swap test:** hide the product name. You can still tell what this is for, and it does not look like every other AI page.
- [ ] **No slop:** nothing from the anti-slop list unless asked.
- [ ] **Real content:** no placeholder text, no broken images, no empty charts.
- [ ] **Nothing broken:** no overlaps, clipped text, sideways scroll on phone, or console errors.
- [ ] **Features intact:** everything that worked before still works.

## Report

In the reply, give the screenshot paths and one line per failed or skipped item. Do not paste the whole list back.
