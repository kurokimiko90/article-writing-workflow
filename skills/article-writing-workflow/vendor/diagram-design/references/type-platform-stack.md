# Platform Stack

**Best for:** the capability inventory of **one** platform, sorted into ordered tiers — a payments platform, an e-commerce middle platform, telco BSS/OSS, a banking core, an internal developer platform. The reader's question is *"what does this thing actually contain, and at which tier does each piece live?"*

The distinguishing claim is **adjacency, not arrows**. A platform stack has no connectors at all: membership and vertical order carry the entire meaning. Sitting in the *business* tier says a capability is composed from the tier below it and is consumed by the tier above it, and that claim holds for every chip in the band without drawing 40 lines to prove it. The moment you need to show that one specific box calls one specific other box, you have left this type.

Not for: abstraction levels with a single named concept per band (**layer stack** — same silhouette, one label per row, a different question); components with real, individual connections (**architecture**); capability blocks owned by *different companies* (**ecosystem**); ordered steps with handoffs (**process**, **data flow**, **swimlane**); pure containment or scope (**nested**).

---

## The grammar — four shapes, four meanings

A platform stack is legible only because the shapes are not interchangeable. Every element is exactly one of these:

| Shape | Treatment | Means |
|---|---|---|
| **Actor pill** — top band, outside the platform frame | `input` fill, `soft` stroke, `rx` = half height | Someone who consumes the platform. Never a capability, never inside a tier. |
| **Capability chip** — 112 × 28 | white fill, `rule-solid` stroke at 0.8 | One bounded capability that has **peers** in the same tier. |
| **Spanning bar** — full tier width, 28 high | `ink @ 0.05` fill, `muted` stroke at 1 | A **single** shared component that everything below it in the tier passes through. |
| **Cross-cutting column** — right side, dashed | `muted @ 0.05` fill, `muted` stroke dashed `4,3` | A tier that serves *every* other tier, so it cannot be stacked with them. |

**A spanning bar is a claim of singularity, not of importance.** One checkout, one orchestrator, one router. If two things do that job, they are two chips — and if you promote a chip to a bar because it's the part you care about, the reader now believes a routing fact that isn't true. Emphasis is what the accent is for.

**The bottom tier is usually not yours.** Bank rails, card networks, carriers, cloud providers — draw that band's chips with the `external` treatment (`ink @ 0.03` fill, `ink @ 0.30` stroke) so the silhouette itself shows where the platform ends.

---

## Canvas and geometry

Canvas `0 0 1200 780`. Everything is on the 4px grid.

| Element | Coordinates |
|---|---|
| Actor band | `x` 40 → 1160, `y` 56 → 120, `rx=8`, no fill, `rule` stroke |
| Platform column (tier bands) | `x` 40 → 932, width 892 |
| Cross-cutting column | `x` 944 → 1160, width 216, `y` 136 → last tier bottom |
| Tier label gutter | `x` 60 → 176 |
| Chip grid | starts `x=180`; column *i* at `180 + 124i`; chip 112 wide, 12 gap; 6 columns end at 912 |
| Spanning bar | `x=180`, width 732 |
| First tier top | `y=136`; 12px between tiers |

**Tier height is a formula, not a judgment call.** A tier holding *n* rows (bars and chip rows count the same) is `20 + 40n` tall: 16px padding, 28px rows, 12px gaps, 16px padding. Row *i* inside a tier starting at `Y` has its top at `Y + 16 + 40i`. One row → 60; two → 100; three → 140. Holding the formula is what keeps six tiers optically even when they hold wildly different amounts of content.

**Cross-cutting entries align to the tiers they sit beside.** Each chip in the right-hand column is vertically centered on one tier band (T2…T5 in the shipped example), never packed into a list at the top. The alignment is what makes the column read as *running alongside* the stack; a block of chips floating in the middle reads as a fifth tier that got moved for space reasons.

**Tier bands:** `rx=8`, fill `ink @ 0.02`, stroke `ink @ 0.10` at 0.8 — quiet enough that 30 chips still read as the figure. Name in Geist 13px/600 in the left gutter, vertically centered, with a mono `T1`…`T6` eyebrow (8px, `0.14em`) above it. The index is what lets someone say "tier 4" out loud in a meeting.

**Ordering is call direction, never importance.** Top is closest to the consumer; bottom is closest to the outside world. If your stack reads top-to-bottom as "most important first", it is a ranked list wearing an architecture costume — use **pyramid**.

---

## Complexity budget

| Limit | Rule |
|---|---|
| Max tiers | 6 |
| Max rows per tier | 3 |
| Max chips per row | 6 |
| Max chips per tier | 12 |
| Max chips in all tiers | 36, zoned |
| Max chips in the cross-cutting column | 4 |
| Max spanning bars | 3 |
| Max actors | 4 |
| Max cross-cutting columns | 1 |
| Max accent elements | 1 |

The chip total is a **zoned exemption** from SKILL.md §7's 9-node limit, on the same terms as **ecosystem**: it is only legal because every chip sits inside a labelled tier that does the grouping work, and because no chip carries a connector. Past 36 chips, split by tier — an overview stack plus one detail diagram for the tier under discussion — never by shrinking the type until the labels stop fitting.

Exactly **one** accent element: the capability the conversation is actually about. Accenting a whole tier band turns the band into a flag and erases the chips inside it; accent a bar or a chip, never a band and never the cross-cutting column.

---

## Anti-patterns

- **Arrows between tiers.** The single most common failure. Adjacency already says "composed from below"; adding arrows converts a clean inventory into a bad architecture diagram with 40 lines and no routing discipline. If the flow genuinely matters, draw a second diagram.
- **A tier with one chip.** Either that thing is shared (make it a bar) or it belongs in the tier above or below. A one-chip tier is a heading pretending to be a layer.
- **Bars used for emphasis.** See above: a bar means "there is exactly one of these", and readers will believe it.
- **A cross-cutting column that only touches two tiers.** Then it is a tier, and it should be stacked like one. The column is reserved for what genuinely spans the whole platform — settlement, identity, observability, billing.
- **Mixed granularity inside one tier.** A product name next to a library next to a team. Everything in a band must be the same *kind* of noun, at the same altitude, or the band stops meaning anything.
- **Actors inside the frame.** People and counterparties are not capabilities. They live in the band above the platform, and keeping them outside is what makes the platform's edge visible.
- **Coloring chips by tier.** Six fills and the hierarchy disappears; the tier band is already the grouping device.
- **Drawing the external providers like your own capabilities.** If the bottom band uses the same white chip as the business tier, the diagram claims you own the card networks.

## Examples

- `assets/example-platform-stack.html` — minimal light
- `assets/example-platform-stack-dark.html` — minimal dark
- `assets/example-platform-stack-full.html` — full editorial
