# Capability Map

**Best for:** the business architecture of **one** platform when its middle is not a flat list — a payments platform, an e-commerce middle platform, a core banking suite, an insurance backbone. The reader's question is *"which domain owns this capability, and what constrains and supports all of them?"*

The distinguishing claim is **the named domain**. A capability map has three levels — tier, domain, capability — and the middle one is the unit people actually point at in a meeting: *transaction center*, *clearing & billing*, *ledger*. A domain has an owner, a roadmap and an on-call rotation; a tier does not. Drawing the domain boundary is what turns forty loose chips into eight things a room can argue about.

Like **platform stack**, it has **no connectors at all** — membership and vertical order carry the entire meaning. Unlike platform stack, it also has **two flanks**, because the concerns that touch every tier come in two kinds and the side they sit on is what tells them apart.

Not for: tiers whose contents are genuinely flat, with no named groupings inside them (**platform stack** — same silhouette, one level less, and the simpler type always wins); abstraction levels with one concept per band (**layer stack**); components with real, individual connections (**architecture**); capability blocks owned by *different companies* (**ecosystem**); pure containment with no ordering (**nested**); ordered steps with handoffs (**process**, **data flow**, **swimlane**).

**Choosing between this and platform stack:** if you can delete every domain name and lose nothing, you had a platform stack. If deleting them makes the middle tier unreadable, you have a capability map.

---

## The grammar — five shapes, five meanings

| Shape | Treatment | Means |
|---|---|---|
| **Tier band** — full core width | `ink @ 0.02` fill, `ink @ 0.10` stroke at 0.8, `rx=8` | One rung of call direction. Named in the left gutter with a mono `T1`…`T5` eyebrow. |
| **Domain box** — inside a tier | `paper` fill, `ink @ 0.20` stroke at 1, `rx=6` | A named, owned bounded context. Title top-left in Geist 12/600. |
| **Capability chip** — 28 high | `paper-2`/white fill, `rule-solid` stroke at 0.8, `rx=4` | One leaf capability. Lives inside a domain, or bare in a tier that has no domains. |
| **Spanning bar** — full domain inner width, 28 high | `ink @ 0.05` fill, `muted` stroke at 1 | The **single** shared component every chip in that domain passes through. |
| **Cross-cutting rail** — a flank column, dashed | `muted @ 0.05` fill, `muted` stroke dashed `4,3`, `rx=8` | A concern that serves every tier, so it cannot be stacked with them. |

**The domain box paints back to `paper`.** The tier band is tinted, the domain plate returns to the page, the chip is brighter again. Three flat fills, no color, and the containment ladder reads at a glance — which is the only reason 40+ chips stay legible.

**A spanning bar is a claim of singularity, not of importance.** One router, one close job. If two things do that job they are two chips, and a reader who sees a bar will believe a routing fact that isn't true. Emphasis is what the accent is for.

**The two flanks are not decoration.** The left rail **constrains** — risk, control, compliance, policy: things that can say no to any tier. The right rail **supports** — merchant admin, contracts, identity, permissions: things every tier consumes. Putting a supporting service on the left, or a control on the right, silently reverses the claim. If you only have one rail, it goes on the side its verb belongs to; if you have neither, you are drawing a platform stack.

**The bottom tier is usually not yours.** Bank rails, card networks, carriers, tax authorities — draw that band's chips with the `external` treatment (`ink @ 0.03` fill, `ink @ 0.30` stroke, `muted` label) so the silhouette itself shows where the platform ends.

**No actor band.** Platform stack puts consumers in pills above the frame; a capability map does not. The top tier *is* the closest thing to the consumer. If who-consumes-it is the question, that is a platform stack.

---

## Canvas and geometry

Canvas `0 0 1200 780`. Everything is on the 4px grid.

| Element | Coordinates |
|---|---|
| Left rail | `x` 40 → 172, width 132 |
| Core column | `x` 184 → 1016, width 832 |
| Right rail | `x` 1028 → 1160, width 132 |
| Tier label gutter | `x` 204 → 320 |
| Tier content area | `x` 336 → 996, width 660 |
| First tier top | `y=56`; 12px between tiers |
| Legend | `y=740` |

**The box grid.** Everything laid out across a tier — domain boxes *and* bare chips — takes its width from one grid. Splitting the 660px content area *n* ways with 12px gaps gives:

| n | 1 | 2 | 3 | 4 | 6 |
|---|---|---|---|---|---|
| width | 660 | 324 | 212 | 156 | 100 |

`n=5` is **not a legal split** — it lands on 122.4 and falls off the grid. Use 4 or 6. Holding one grid for both boxes and chips is what makes a tier of domains and a tier of bare chips look like the same diagram.

**Row heights are a formula, not a judgment call.**

| Row | Height |
|---|---|
| Bare chip row | 28 |
| Inline domain (a domain flat enough to be one row) | 60 |
| Domain box holding *k* rows | `52 + 40k` — 92, 132, 172, 212 |

A tier holding *m* rows is `32 + Σheights + 12(m−1)` tall: 16px padding, rows, 12px gaps, 16px padding. Side-by-side domain boxes in one row are **padded to equal height** — unequal heights read as unequal importance, which is a claim you did not mean to make.

**Inside a domain box:** 12px padding; title baseline at `boxY + 30`; row *m* top at `boxY + 48 + 40m`. A spanning bar occupies a whole row at `x = boxX + 12`, width `boxW − 24`. Chips split the inner width: `(boxW − 24 − 12(k−1)) / k`, and the result **must** land on the 4px grid — for a 324 box that means k=2 (144) or k=3 (92); for a 660 box, k=2 (312), k=3 (204) or k=6 (96).

**Inside an inline domain:** the name sits at `boxX + 16` in a 112px gutter, chips start at `boxX + 128`, and the chip area is `boxW − 144`. At full width that is 516 — k=2 (252), k=3 (164), k=4 (120) or k=6 (76).

**Rails span the whole tier stack**, top of T1 to bottom of the last tier. A 56px title block holds a mono eyebrow (`CONSTRAINS` / `SUPPORTS`) and the rail name in Geist 12/600; the chip zone is the remaining height minus 16px of bottom padding. Rail chips are 108 wide, and their height is `min(96, ⌊(Z − 12(k−1)) / k⌋)` rounded down to the grid, with the leftover redistributed as even gaps. Chips **fill the rail** — a short stack packed at the top reads as a tier that got moved for space reasons, which is the one thing a rail must not look like.

**Ordering is call direction, never importance.** Top is nearest the consumer, bottom is nearest the outside world. A stack that reads top-to-bottom as "most important first" is a ranked list wearing an architecture costume — use **pyramid**.

---

## Complexity budget

| Limit | Rule |
|---|---|
| Max tiers | 5 |
| Max domains per tier | 5 |
| Max domains total | 8 |
| Max chips per domain | 9 |
| Max chips in the tier stack | 44, zoned |
| Max rails | 2 — at most one per flank |
| Max chips per rail | 6 |
| Max spanning bars | 2 |
| Max accent elements | 1 |
| Connectors | 0, always |

The chip total is a **zoned exemption** from SKILL.md §7's 9-node limit, on the same terms as **ecosystem** and **platform stack**, and it is a wider one because the grouping is stronger: every chip sits inside a named domain inside a labelled tier, and no chip carries a connector. Past 44 chips, split by domain — an overview map plus one detail diagram for the domain under discussion — never by shrinking the type until the labels stop fitting.

Exactly **one** accent element: the capability the conversation is actually about. Accent a chip or a bar. Accenting a domain box turns its whole contents into a flag; accenting a tier band or a rail erases everything inside it.

---

## Anti-patterns

- **Arrows between tiers or domains.** The single most common failure. Adjacency already says "composed from below"; adding arrows converts a clean inventory into a bad architecture diagram with 40 lines and no routing discipline. If one specific path matters, it earns its own **sequence** or **data flow**.
- **A domain box with one chip.** That is a chip with a title bar. Either it has peers and belongs beside them, or the domain name *is* the capability — drop one of the two levels.
- **A tier with exactly one domain.** The domain boundary and the tier boundary now claim the same thing twice. Merge them, or find the domain's sibling.
- **Naming domains after teams.** *Platform team* is not a bounded context; it is this quarter's org chart, and it will be wrong before the diagram is shared. Name the capability the domain owns. If ownership is the actual subject, use **org chart**.
- **Rails on the wrong flank.** Left constrains, right supports. A shared-services rail on the left claims that provisioning can veto a payment.
- **A rail that only touches two tiers.** Then it is a tier and should be stacked like one. Rails are for what genuinely spans the platform — risk, identity, observability, billing.
- **Mixed granularity inside one domain.** A product name next to a library next to a vendor. Everything inside a box must be the same *kind* of noun at the same altitude, or the box stops meaning anything.
- **Coloring domains to tell them apart.** Eight fills and the containment ladder disappears; the box outline is already the grouping device.
- **Drawing external providers like your own capabilities.** If the bottom band uses the same chip as the core tier, the diagram claims you own the card networks.

## Examples

- `assets/example-capability-map.html` — minimal light
- `assets/example-capability-map-dark.html` — minimal dark
- `assets/example-capability-map-full.html` — full editorial
