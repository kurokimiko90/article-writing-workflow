# Concept Panorama

**Best for:** the one image that teaches a whole conceptual domain to a reader who does not yet have its vocabulary — *how an AI system actually works*, *how our platform turns a lead into revenue*, *what "observability" is made of*. It is the diagram that gets pinned in a wiki, opens a talk, or onboards a new hire. The reader's question is *"what are the moving parts, which ones sit on the path, and which ones sit underneath it?"*

The distinguishing claim is **the question line**. Every block carries, directly under its name, the question that block answers: *AI knows what? · what may it look at this time? · how do we prove it got better?* A panorama is a piece of teaching, and the questions — not the boxes — are what the reader takes away. A block whose question you cannot write is not a concept; it is an implementation detail that belongs in someone's bullet list.

The second claim is **band membership**. Blocks on the **spine** happen on the request path, in order, once per run. Blocks in the **support band** persist across runs — they remember, constrain, observe and improve the spine, but they are not steps in it. Every block sits in exactly one band, and any block you cannot confidently place is the block to cut.

Not for: a system's real components and their real calls (**architecture**); one ordered path with no substrate under it (**process**, **data flow**); capabilities sorted into tiers with no arrows at all (**platform stack**, **capability map**); a cycle whose whole point is that it closes (**loop**); one concept per band with nothing inside (**layer stack**); two competing ways of working (**contrast panels**).

**Choosing between this and process:** if you delete the support band and the diagram still answers the reader's question, you had a process. If deleting it removes the memory, the guardrail and the feedback — the reasons the thing works twice — you have a panorama.

---

## The grammar — four shapes, two lines, one verb

| Element | Treatment | Means |
|---|---|---|
| **Concept card** — vocabulary band, top | `paper-2`/white fill, `rule-solid` stroke at 0.8, `rx=6`, mono index badge | One named term the rest of the diagram will use. Numbered, never connected. |
| **Spine stage** — middle band | `paper`/white fill, `ink` stroke at 1, `rx=6` | One step on the request path. Carries an icon and one bullet block. |
| **Support block** — lower band | `ink @ 0.03` fill, `ink @ 0.20` stroke at 0.8, `rx=6` | A mechanism that persists across runs. Tinted as a band so the substrate reads as ground, not as more steps. |
| **Bullet block** — inside any block | mono eyebrow at 8px + 3–4 bullets in Geist 10 | The concrete instances behind an abstraction. The eyebrow names the *kind* of list (`TECHNIQUES`, `MECHANISMS`, `WHAT WE WATCH`). |
| **Spine connector** | solid, `muted`, `marker-end="url(#arrow)"` | Forward movement along the path. Only the spine has these. |
| **Support connector** | dashed `5,4`, `soft` or `muted` | Feeds, governs, observes, returns. Never solid, never on the spine. |

**Two line kinds, and only two.** Solid means *the run moves forward*; dashed means *something off the path touched it*. A third stroke style — dotted, thick, colored — is the moment a panorama stops teaching and starts being an architecture diagram with 40 lines and no routing discipline.

**Every dashed connector carries a one-word verb.** `FEEDS`, `TRACKS`, `GOVERNS`, `SUPPLIES`, `OBSERVES`, `SCORES`, `CURATES`. The verb is the only thing that tells the reader whether a support block *serves* the stage or *constrains* it, and those are opposite claims. An unlabelled dashed line reads as vague association, which is exactly what a teaching diagram must not contain. Spine connectors are usually unlabelled — adjacency plus the stage names already say "then".

**The support band's empty columns are its wiring channels.** A support block sits under the stage it serves, and its riser is a straight vertical line in its own column. When a block on the second support row must reach the spine, it rises through a column no first-row block occupies. If you cannot find a free lane, the support band is trying to be a second spine — merge blocks or cut one.

**The vocabulary band is optional and never connected.** It names terms; the numbering carries the ordering claim, and column alignment pairs each card with the stage below it. The moment you draw an arrow from a card to a stage you have said the card is a step, and the reader will spend the rest of the diagram looking for the card that matches every other box.

---

## Canvas and geometry

Canvas `0 0 1400 1120`, margins 40. Everything is on the 4px grid, and every band shares **one column grid** — that shared grid is what makes a card, a stage and a support block read as three views of the same six things.

| Element | Coordinates |
|---|---|
| Content area | `x` 40 → 1360, width 1320 |
| Column *k* (of 6) | `x = 40 + 228k`, width 180 |
| Vocabulary band | `y` 24 → 224, card height 200 |
| Spine band | `y` 256 → 576, stage height 320 |
| Spine connectors | `y=416`, in the 48px column gaps |
| Support row 1 | `y` 640 → 840, height 200 |
| Support row 2 | `y` 872 → 1048, height 176 |
| Legend | hairline at `y=1068`, labels at `y=1084` |

**Column splits.** A band with fewer than six blocks uses the same content width and a legal split:

| n | 3 | 4 | 5 | 6 |
|---|---|---|---|---|
| gap | 48 | 40 | 40 | 48 |
| width | 408 | 300 | 232 | 180 |

**Spanning.** A support block may span *s* adjacent columns: `width = 228s − 48`, starting at its leftmost column's `x`. Spanning is how a block earns visual weight honestly — a feedback loop that contains a four-step micro-strip is genuinely wider than a memory block, and stretching it to span three columns says so without color.

**Inside a spine stage** (180 × 320): name baseline at `y + 28` (Geist 13/600); question line at `y + 48` (Geist 9.5, soft — a question is human-readable, so it is never set in mono); icon centered at `(x + 90, y + 100)` in a 40px box; bullet-block eyebrow at `y + 188` (mono 8); bullets at `y + 208`, `+228`, `+248`, `+268` (Geist 10, marker dot at `x + 19`, text at `x + 30`).

**Inside a concept card** (180 × 200): index badge `16 × 12` at `(x + 12, y + 14)`; term baseline `y + 34`; question at `y + 54` (mono 8.5, soft, wrapped to at most two lines); icon centered at `(x + 90, y + 108)`; one or two instance lines centered at `y + 156` and `y + 174`.

**Inside a support block:** name baseline at `y + 28`; question at `y + 48`; eyebrow at `y + 76`; bullets on a 20px rhythm from `y + 96`. **Support blocks carry no icon.** The glyph is a spine-and-vocabulary device; giving the substrate icons too flattens the three bands back into one wall of cards. A block that spans two or more columns splits its bullets into two columns rather than growing taller — support rows are padded to equal height, because an uneven support band reads as uneven importance.

**The micro-strip** (at most one per diagram): a four-step chain drawn *inside* one support block — 132-wide step boxes on 20px gaps, a 24px glyph centred in each, label beneath in Geist 9.5, and 14px solid connectors in the gaps. It is the only place a solid line appears outside the spine, and it is legible as internal because it never crosses the block's border. Use it when one support block is itself a small process — human correction → labelling → dataset → retrain. A second micro-strip and the diagram has two subjects.

**A label mask that lands on the support band needs two rects.** The band ground is `paper` plus a tint, so a single `paper`-filled mask punches a visibly lighter hole in it. Paint the mask twice — `paper`, then the same band tint over it — and the label sits on ground that matches exactly. Bands are painted before connectors, so this is the one mask in the type that is not a plain paper rect.

**Band eyebrows sit above their band, and must clear the riser labels.** A long band eyebrow at the left margin collides with the verb on the first riser; keep them to one or two words (`SUPPORT BAND`) and let the legend carry the sentence.

---

## Complexity budget

| Limit | Rule |
|---|---|
| Max bands | 3 |
| Max spine stages | 6 |
| Max concept cards | 6 — never more than the stage count |
| Max support blocks | 8, in at most 2 rows |
| Max bullets per block | 4 |
| Max solid connectors | stages − 1 |
| Max dashed connectors | 8 |
| Max micro-strips | 1, of at most 4 steps |
| Max accent elements | 2 |
| Legend | mandatory, always |

The block total is a **zoned exemption** from SKILL.md §7's 9-node limit, on the same terms as **ecosystem** and **capability map**: every block sits in a labelled band on a shared column grid, no block carries more than one connector per direction, and the two line kinds are legended. Past 6 stages or 8 support blocks, split — one panorama plus a detail diagram of the stage under discussion — never by shrinking the type until the questions stop fitting.

The legend is mandatory here, unlike most types, because the panorama makes two claims a reader cannot recover from the shapes alone: solid versus dashed, and what the tinted band means.

---

## Anti-patterns

- **Rainbow-coding the blocks.** One hue per stage, repeated on the matching concept card, is the single most common way this diagram is drawn — and it burns the entire palette to encode information that column alignment already carries for free. Six colors and the accent no longer means anything; keep one tint per *band*, pair cards to stages by column and number, and spend the accent on the one or two blocks the conversation is actually about.
- **Solid arrows out of the support band.** The instant a support block gets a solid connector it becomes a step, and the reader starts asking when it runs. Memory does not run after retrieval; it is underneath the whole thing.
- **A support block fanned to every stage.** Six dashed lines from one block is not a claim, it is a shrug. If it genuinely serves everything, say so once — in its question line or the legend — and draw the one riser that matters.
- **A block without a question.** The question line is the type. A block reduced to a noun and a bullet list is a table row that has been given a border.
- **Bullets that are sentences.** Two to four words each. The block name and the question carry the argument; the bullets are evidence, not prose.
- **A branching spine.** The spine is linear by definition. A fork means a decision, and decisions belong in a **flowchart**.
- **Vocabulary cards that are not concepts.** A product name, a vendor, a team. The top band defines the words the diagram uses; filling it with brands turns a teaching diagram into a logo wall.
- **Arrows between concept cards.** They are a glossary, not a pipeline. If they are ordered steps, they were the spine all along and you have drawn the same row twice.
- **A panorama with an empty support band.** Two bands and no substrate is a **process** with a glossary on top. The support band is the reason this type exists.
- **Risers that cross support blocks.** Route through a free column. A dashed line passing behind a block it does not touch claims a relationship that is not there — see SKILL.md §6 rule 5.

## Examples

- `assets/example-concept-panorama.html` — minimal light
- `assets/example-concept-panorama-dark.html` — minimal dark
- `assets/example-concept-panorama-full.html` — full editorial
