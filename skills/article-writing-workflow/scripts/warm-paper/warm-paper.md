<!-- diagram-design-profile
name: Warm Paper
slug: warm-paper
source-url: none
created: 2026-10-16
updated: 2026-10-16
notes: article-writing-workflow — mirrors article-figures templates/warm-paper so knowledge diagrams and article figures share one look. Structure/geometry rules unchanged from pdm-flat; only the skin differs.
-->
# Style Guide

**The single source of truth for colors, typography, and tokens.** Every diagram draws from this.

Custom skin: **Warm Paper** — same palette as `<skill>/../article-figures/` default style `warm-paper`, so G2 knowledge diagrams and stage-07 article figures read as one set.

## Skin rules (apply on top of the type references)

- Page background: flat warm paper `#F6F2EA` + faint paper noise. **No apricot / lime radial gradients** (2026-10-22 user correction: corner glows read as random highlights; delete `body::before` radial-gradient when reusing an older diagram as template). The SVG itself has **no full-canvas background rect** (use `fill="none"`), so the paper shows through. Polish deletes any rect at the origin (x/y missing or 0) that is ≥1000 wide and ≥300 high, whatever its fill. A white or card-colour panel behind the whole diagram is a defect (2026-10-21: ja story 01–03).
- Nodes: card fill `#FFFCF6`, corner radius 14 (SVG units), hairline `rgba(31,42,39,0.08)` stroke + soft drop shadow (`feDropShadow dy=4 std=6 #5a4a32 @ .10`). No dark 1px outlines.
- Focal box (1 per diagram): fill `mark-soft #EEF6C8`, stroke lime `#C3DB3E`. Focal text / focal arrows use `accent` (teal).
- Title: one short sentence above the SVG, 38px / weight 900. `<mark>` lime highlighter (`linear-gradient(transparent 52%, #D9F05B 52% 92%, transparent 92%)`) is **optional**: use it on at most one genuine key word, never mechanically on “the part after the first `：` `；` `，`”. No key word → no highlight (2026-10-22 user correction).
- Legend wording: say 绿色 (not 蓝色) for the focal fill.
- Fonts: `Noto Sans SC` (Simplified Chinese, `font-feature-settings: normal`, letter-spacing .03em) or `Zen Kaku Gothic New` (Japanese, `palt`). `Geist Mono` only for stage numbers / tags. No serif italics — callouts use sans 500.
- Start / human-input boxes (起点、问题、人类决定 G1–G3、限制): apricot tint `#FCEFE4` + stroke `rgba(242,169,126,.55)`, only when the diagram really needs to separate the human role; otherwise use a normal card. Legend wording 杏色框, not 灰框.
- **Colour budget** (2026-10-22 user correction “颜色超多”): per diagram at most neutral cards + teal lines + one focal colour (+ apricot only when the human role must be distinguished). No decorative colour.
- All rect borders are hairlines (`rgba(31,42,39,.14)`); no dark grey outlines. Small labels: sans 16px, letter-spacing .04em (no mono for Chinese). Callout sentence: teal, weight 700.
- **Minimum font size 16px (SVG units)** — the 1280-wide viewBox is shown at ~880px in articles, so anything smaller is unreadable. Polish raises every smaller size to 16; design for 16 from the start: card width ≥ longest line × 17 + 32, stacked lines ≥ 1.4 × font size apart, short copy (Japanese runs ~30% longer than Chinese).
- **Spacing gate** — after the screenshot, the build checks every text for overlap with other text or badges, overflow from its card, line spacing < 1.25× font size, and legend swatches closer than 6px. Any hit prints `× 間隔の問題` and the build exits 1. Fix by shortening/splitting copy or widening the box; never by shrinking text. Auto-fixes already applied: stacked lines spread to 1.4×, pill rows (rx = h/2, h ≤ 44, gaps < 30) resized to their text, legend items re-laid left-to-right by real text width.
- Title: 36px, `text-wrap: balance` so no single-character orphan line.
- PNG export: whole page (title + SVG, eyebrow/deck/foot hidden) at 1360px width @2x; SVG viewBox auto-cropped to content bbox; window height = measured `<main>` height.

## Scripts

**Standard: one command** — `python3 warm-paper-build.py <diagrams_dir> [file.html…]` runs steps 1–4 below (convert only if the file is still pdm-flat), applies `badges.json` if present, warns when a title exceeds 16 full-width chars, fails (exit 1) when a badge cannot be placed (pin it with `cx`/`cy` instead), and finally runs `figure-lint.py` (lime double focus, `palt` on Chinese, untranslated Chinese in Japanese figures, numbers/words not in the article, translated-vs-source structure, over-wide UI screenshots). Titles: ≤16 chars; `<mark>` optional, one genuine key word at most. In-SVG eyebrow/heading (`.ey`/`.hd`) are hidden in the PNG.

Individual steps (run in order)

1. `python3 warm-paper-convert.py <file.html>…` — only for legacy pdm-flat diagrams (palette swap).
2. `python3 warm-paper-polish.py <file.html>…` — hairlines, apricot start boxes, 16px font floor, mask fix, auto line-spacing / pill / legend relayout, auto-crop and spacing-check script. Safe to re-run.
3. `python3 warm-paper-badges.py <dir>/badges.json` — round lucide icon badges; preferred entry form `{"anchor": "text inside the card", "icon": "...", "tone": "..."}` (auto-placed inside the card without covering text; same-size card groups share one position, or the whole group is skipped with a warning) (tones: apricot = human/start, teal = facts/AI, lime = the one focal item, neutral = gaps/contrast, ink). Positions are hand-picked per diagram in `badges.json` so they never cover text: inside the card left of a centred title, top-right of a left-aligned card, or right end of a layer row; `"under": true` puts a circle behind an existing icon. Icons cached in `icons/` next to the scripts (lucide-static@0.469.0). Safe to re-run.
4. `python3 warm-paper-shoot.py <file.html>…` — writes `<file>.png`, prints spacing problems and exits 1 if any.

After step 4, open each PNG and check legend wording still matches the colours (e.g. a legend swatch may need manual correction).

## Tokens

| Role | Purpose | Light |
|---|---|---|
| `paper` | Page background | `#F6F2EA` (warm paper) |
| `paper-2` | Lane / container fill | `#EFE9DD` (or `rgba(31,42,39,0.02)`) |
| `card` | Node fill | `#FFFCF6` |
| `ink` | Primary text | `#1F2A27` |
| `muted` | Secondary text | `#5E6B66` |
| `arrow` | Default arrow stroke | `#7D857F` |
| `soft` | Sublabels | `#8E948D` |
| `rule` | Hairline borders | `rgba(31,42,39,0.12)` |
| `rule-solid` | Baselines | `#E6DFD2` |
| `accent` | Focal text / arrows (teal, facts & links) | `#11645B` |
| `link` | Deep teal | `#0E5048` |
| `mark` | Highlighter: one focus per diagram. Title `<mark>` and the in-diagram focal box must point at the same message; if they differ, drop the title mark (2026-10-26 review: this was the most repeated finding across 4 articles) | `#D9F05B` |
| `mark-soft` | Focal box fill | `#EEF6C8` |
| `mark-line` | Focal box stroke | `#C3DB3E` |
| `apricot` | Secondary warm accent (badges, rare) | `#F2A97E` |

Dark mode is not defined for this skin (article PNGs are light only).

Converter for legacy pdm-flat diagrams: re-map hex values per this table (navy→ink, royal-blue→teal, blue tint→mark-soft, white→card) — script: `warm-paper-convert.py <file.html>…`.
