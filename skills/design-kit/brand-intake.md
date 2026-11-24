# Brand intake

Use this when the user hands over a brand guide, a website, a logo, a color list or an existing app, and the project has no `DESIGN.md` yet. The goal is one short file that every design skill reads, so the brand is captured once.

## Read the source

Take whatever is given: a PDF or doc, a URL, a Figma or token export, a list of hex codes, an existing CSS theme, or screenshots. Pull out only what changes how things look or sound. If a value is missing, write a sensible default and mark it `(default)`. Do not ask a question unless a missing value would change the whole look.

## Write `DESIGN.md` at the project root

Keep it under about 60 lines. Use this shape:

```markdown
# Design

Source: <link or file name of the brand guide>

## Brand
- Colors: primary #..., secondary #..., neutrals #... / #..., success #..., warning #..., danger #...
- Type: headings <font>, body <font>, numbers/code <font>
- Shape: corner radius <px>, borders <thin/none>, shadows <none/soft>
- Logo: <where and how it may appear>
- Voice: <three words>, e.g. plain, confident, warm

## Look
- Style: <style name from design-kit/styles or a custom one>
- Density: <airy / balanced / dense>
- One bold move: <the single distinctive choice>

## Pages
<!-- add one line per page that differs from the default -->
- Dashboard: dense, status first, dark side nav
- Home: airy, one call to action

## Never
- <brand rules that must not be broken>
```

## After writing

Tell the user in one line that `DESIGN.md` was created and what style it uses. Later design skills update the **Look** and **Pages** sections when the user picks a direction. They never change **Brand** unless the user gives a new guide.

Privacy: `DESIGN.md` belongs to the project. Never copy a client's brand into the skills repo or into your personal folder.
