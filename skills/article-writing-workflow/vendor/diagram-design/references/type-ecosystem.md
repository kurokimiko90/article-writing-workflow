# Ecosystem

**Best for:** a value chain that crosses **organizational** boundaries — payments and settlement, supply chains, insurance claims, ad tech, healthcare claims, open banking. Use when several *independent* institutions each run their own internal machinery, and the reader's question is "who holds the thing at each step, and what actually crosses the boundary between them?"

The distinguishing claim is that a boundary here is a **counterparty**, not a subsystem. Two blocks named "ledger core" in two different institutions are two different ledgers owned by two different companies, reconciled by contract rather than by a shared database — and that fact is the whole reason the diagram exists.

Not for: one company's internal system (use **architecture**), containment or scope with no flows (use **nested**), a role-scoped pipeline inside one organization (use **data flow** or **swimlane**), or a time-ordered message trace between named parties (use **sequence** — an ecosystem map is deliberately *not* a timeline).

---

## Layout conventions

- **Canvas:** `0 0 1200 800`. Institutions occupy `x` 220 → 956; the columns outside — `x` 40 → 180 and `x` 1020 → 1160 — are reserved for the **actors** who are not institutions (a cardholder, a patient, a shipper). Keeping people outside every boundary is the point: they are the only participants who belong to no one.
- **Institution zone:** `rx=8`, `zone-fill`, `zone-stroke`, `stroke-width=1`, drawn **before** every connector. Its name is a `soft` mono eyebrow (8px, `0.18em`) centered on the **top border**, masked, so the border reads as continuous. Zones paint first, so an edge label may legally sit on a zone border.
- **Bands, not a grid.** Stack institutions as full-width horizontal bands in settlement order (who holds the value first → who holds it last), 176px apart: a 120px band leaves a **56px corridor** below it. That corridor is where every label lives. Two peer institutions at the same stage sit side by side in one band (`220 → 572` and `604 → 956`), which is how the map says "these two never talk to each other directly."
- **Capability blocks** sit inside a zone with 28px padding on all sides and 40px between blocks: three 200px blocks, or two 320px blocks, per band. Each carries a **role tag** — a `rx=2` rectangular mono chip, ≤4 characters, top-left — because the same noun ("core", "switch") means something different in each institution and the tag is what disambiguates it.
- **Leaf account rows** — the ledger accounts a bank actually holds — use the store treatment (`ink @ 0.05` fill, `muted` stroke), a 48px height, and **no role tag**. They are balances, not capabilities, and the missing tag is what says so.
- **Focal:** exactly **two** accent blocks — the one that owns the decision and the one that owns the money. Never accent an institution zone; a boundary is context, and accenting it turns the whole band into a flag.

## Flow taxonomy — the part that makes this type work

A single arrow style collapses the one distinction the reader came for. Every connector is one of three kinds, and the legend names all three:

| Flow | Stroke | Means |
|---|---|---|
| **Instruction** | `muted`, 1.2 | A message: an order, an authorization request, a clearing file. Travels in seconds. |
| **Funds** | `link`, 1.4 | Actual money moving between accounts. Travels in days. |
| **Account relation** | `soft`, 1, dashed `4,3` | A standing bookkeeping fact — *this ledger mirrors that account*, *this person owns that account*. Not an event, and never on the critical path. |

**Never merge an instruction and the funds it eventually causes into one arrow.** They leave together and land days apart; drawing them as one line is the single most common way these maps lie. If a reader can't tell from the diagram that authorization and settlement are different events, the diagram has failed regardless of how clean it looks.

Give each flow a verb label in mono 8px, ≤14 characters, tinted to its own flow color (`muted` / `link` / `soft`) so the strip and the stroke agree. Labels go in the corridors, never inside a zone body.

## Routing

The band layout makes most connectors vertical drops through a corridor — a straight `<line>` is correct when source and destination share an `x`. Everything else follows SKILL.md §6 unchanged: rounded right-angle elbows at `r=8`, 6–10px label gaps, fanned attach points, no overlaps.

Two routes are specific to this type:

- **Return legs run outside every zone.** Money coming back to where it started (settlement → merchant wallet, reimbursement → provider) routes up the free column at `x=992`, outside the `956` zone edge, and re-enters its destination on the *right* edge. Cutting back up through the bands means crossing three boundaries that the funds never actually touch.
- **Aligned columns beat centered attach points.** When one instruction descends through three institutions, hold it at a single `x` the whole way down even where that x is off-center in a wide block. The column *is* the reading: this is one authorization, handed down.

## Complexity budget

| Limit | Rule |
|---|---|
| Max institutions (zones) | 6 |
| Max blocks per institution | 4 |
| Max blocks total | 14 |
| Max external actors | 2 |
| Max connectors | 12 |
| Max accent blocks | 2 |

The block total is a **zoned exemption** from SKILL.md §7's 9-node limit, on the same terms as the `faithful` detail level: it is only legal because every block sits inside a labelled boundary that does the grouping work. Past 14 blocks, split by flow — one map for authorization, one for settlement — never by institution, which just hides the boundary crossings the diagram exists to show.

## Anti-patterns

- **One arrow style for everything.** Instruction, funds, and account relations become indistinguishable and the map degrades into a generic box-and-line drawing.
- **Reading the bands as a timeline.** These are institutions, not steps. If your content is genuinely time-ordered between named parties, it is a **sequence** diagram.
- **Nesting an institution inside another.** Only regulators and scheme operators contain other parties, and even then containment misstates the relationship — use a boundary-crossing flow.
- **Modeling failure paths on the happy-path map.** Declines, chargebacks, returns, and reversals each retrace the whole map backwards; they belong in a second diagram.
- **Interbank arrows that skip the scheme.** If clearing goes through a network, drawing bank → bank is factually wrong, and it is exactly the error a domain reader will catch first.
- **Accenting every core.** Every institution has a core. Two of them matter.
- **An unlabelled boundary.** A zone whose name is implied by its contents is a rounded rectangle doing nothing.

## Examples

- `assets/example-ecosystem.html` — minimal light
- `assets/example-ecosystem-dark.html` — minimal dark
- `assets/example-ecosystem-full.html` — full editorial
