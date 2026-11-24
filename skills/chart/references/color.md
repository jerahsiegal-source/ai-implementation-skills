# Chart color

## Where the colors come from

1. **The project's `DESIGN.md`.** If it has a **Chart** section or line with hex codes, use those.
2. **The user's personal taste** (`~/.ai-skills/personal/taste.md`), if it names chart colors.
3. **The default palettes below.**

Whatever the source, run the palette check on the page's background before using it:

```
node scripts/check-palette.mjs "#245080,#7E4D28,#0F835B" --bg "#FFFFFF" --bg2 "#12181D"
node scripts/check-palette.mjs --from DESIGN.md --bg "#F7F8F6"
```

It fails a color that is under 3:1 on the background, two colors that look nearly the same, and pairs that blur together for protanopia or deuteranopia (red-green color blindness). If brand colors fail, keep the brand color for the one highlighted series and pick the others to pass. Say so in one line.

## Default palettes

These pass `check-palette.mjs`. Use them in order; series 1 is the highlight.

| Role | Light (on #FFFFFF) | Dark (on #12181D) |
|---|---|---|
| Series 1 | `#245080` blue | `#487ABB` |
| Series 2 | `#7E4D28` brown | `#BC7F4F` |
| Series 3 | `#0F835B` green | `#70EEB6` |
| Series 4 | `#840B47` wine | `#E073B6` |
| Series 5 | `#5F21B7` violet | `#A070DA` |
| Series 6 | `#A97D1B` ochre | `#DAC66E` |
| Context (gray) | `#B9C2C9` | `#4A5661` |

Past six series, don't add colors. Highlight and gray, group the rest as "Other", or split into small multiples.

## Patterns

- **Highlight:** the series that matters in series 1, everything else in the context gray. Label the highlight in bold.
- **Good and bad:** use the project's status colors for status only, and always pair with a word or icon.
- **Sequential (low to high):** one hue from light to dark. In light mode, light means low.
- **Diverging (below and above a middle):** two hues meeting at a neutral gray at the meaningful middle (zero, target, average).
- **Dark mode:** switch to the dark column. Don't reuse light colors on a dark background.
