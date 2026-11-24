# Quality check

Run this before handing any visual work back. Inside a work loop, the screenshots and this list are the evidence for every design item.

## How

1. Render the real thing: open the page, run the app, or open the HTML file in a browser (Playwright or the tool's browser).
2. Screenshot at desktop width (about 1280px) and phone width (about 400px). If the page has dark mode, check both themes.
3. Go through the list below. Fix what fails, then take one more look. Do not loop more than twice; report anything left.

## The list

- [ ] **5-second test:** the most important thing on screen is obvious without reading.
- [ ] **One focal point** per view. Nothing else competes with it.
- [ ] **Hierarchy:** headings, numbers and actions are clearly ranked by size, weight and position.
- [ ] **Floor:** readable text, contrast, icon plus word for status, focus states ([floor.md](floor.md)).
- [ ] **Fits the surface:** density and layout match the surface notes (busy dashboard is fine, busy landing page is not).
- [ ] **Brand and style:** colors, type and tokens come from `DESIGN.md` or the chosen style, not random values.
- [ ] **No slop:** nothing from the anti-slop list unless asked.
- [ ] **Real content:** no placeholder text, no broken images, no empty charts.
- [ ] **Nothing broken:** no overlaps, clipped text, sideways scroll on phone, or console errors.
- [ ] **Features intact:** everything that worked before still works.

## Report

In the reply, give the screenshot paths and one line per failed or skipped item. Do not paste the whole list back.
