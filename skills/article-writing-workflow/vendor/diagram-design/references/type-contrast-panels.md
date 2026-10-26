# Contrast Panels

**Best for:** an argument that a **mechanism** has to change — the old way of working versus the proposed one, the current escalation path versus the redesigned one, manual reconciliation versus the automated close. The reader's question is *"what actually gets rewired, and why is the new wiring better?"*

The distinguishing claim is **one cast, two wirings**. The same actors — the same operator, the same agent, the same artifact — appear in both panels, and only the connections between them differ. That constancy is the whole argument: it says *nothing was added and nobody was replaced; the work was routed differently*. A reader who can point at the same figure on both sides and trace two different paths through it has understood the proposal without reading a word of the deck around it.

This is also the reason it survives SKILL.md §2's standing rule that **simple before/after belongs in a table**. A table compares *attributes* — cost, headcount, latency — and it does that better than any drawing. It cannot show that the review step moved from after the artifact to during it. If your two columns are attribute lists, close this file and write the table.

Its second device is the **icon-node**: a glyph with a label under it and no box around it. Every other type in this skill draws boxes, because every other type is describing structure. Contrast panels describes *conduct* — who does what, in what order — and a boxed org of pictograms reads as an architecture diagram that happens to have pictures in it. The glyph is the node.

Not for: change in a **quantity** between two states (**slopegraph** — the numbers are the story, and a picture of them is a worse picture); one cycle examined on its own (**loop**); one mechanism drawn once, in stages (**process**, **data flow**, **swimlane**); a legacy landscape inventoried without a proposed replacement (**IT current-state**); three or more states sampled along a time axis (**timeline**).

**Choosing between this and slopegraph:** if the two panels would still make the argument with every number deleted, you have contrast panels. If deleting the numbers empties them, you have a slopegraph.

---

## The grammar — six shapes, six meanings

| Shape | Treatment | Means |
|---|---|---|
| **Panel** — one half of the canvas | No fill, no border. A bracket tag plus a name on one baseline, over a `rule-solid` hairline at 0.8 | One complete mechanism. Panels are separated by whitespace and one dashed divider, never by a box. |
| **Icon-node** — a 48px glyph | `currentColor` at `ink`, `stroke-width = 1.5 / scale`, name in Geist 12/600 below, optional mono 9 sublabel | An actor, a tool, or an artifact. No box, ever. |
| **Ring** — a circle of arcs around a hub | `muted` at 1.2, 3–4 arcs with `arrow` markers, 12° gaps at the stations | A cycle inside one panel. The hub is a 48px glyph; stations are 24px glyphs sitting on the circle. |
| **Ghost cluster** — any node or ring at `opacity 0.35` | All strokes `muted`, labels `soft` | Something the new mechanism supersedes but has not deleted. |
| **Consequence meter** — a 240×16 track, `rx=8` | `ink @ 0.06` fill, `rule-solid` stroke 0.8, filled portion in `ink`, value in mono 11/500 | The outcome the mechanism produces, stated once per panel in one shared unit. |
| **Divider** — a dashed vertical hairline in the gutter | `rule-solid` dashed `4,4` at 0.8, `opacity 0.5` | The gutter. It exists to say *no connector crosses here*. |

**The cast must be shared, and it must be visibly shared.** If the operator is a `user` glyph on the left, it is the same `user` glyph on the right — same icon, same name, same label wording. Swapping the glyph for a synonym across the gutter breaks the only device the type has.

**Ghosts belong to the panel that supersedes them.** A ghost in the *before* panel is incoherent: nothing has replaced it yet. Draw one ghost cluster at most, in the *after* panel, and only when the old mechanism genuinely survives — most proposals do not actually delete the thing they route around, and drawing that honestly is what stops the after panel from reading as a fantasy.

**Meters are evidence, not decoration.** Both panels state the **same metric in the same unit on the same track length**, so the two filled bars are directly comparable at a glance. Two panels measuring different things is not a contrast; it is two facts printed near each other.

**Nothing crosses the gutter.** No arrow, no bracket, no "→" between the panels. The title carries the direction of travel; a connector across the divider quietly turns two competing claims into one pipeline, which is the opposite of the argument.

---

## Canvas and geometry

Canvas `0 0 1200 760`. Everything is on the 4px grid; ring-arc endpoints are the sole exception, since they land where the circle puts them.

| Element | Coordinates |
|---|---|
| Panel A | `x` 40 → 576, width 536 |
| Gutter / divider | `x` 576 → 624, divider at `x=600`, `y` 48 → 700 |
| Panel B | `x` 624 → 1160, width 536 |
| Panel header baseline | `y=60` — bracket tag at the panel's left edge, name at `+88` |
| Header hairline | `y=76`, full panel width |
| Scene area | `y` 100 → 620 |
| Consequence band | eyebrow `y=656`, meter track `y` 664 → 680 |
| Legend | hairline `y=716`, label baseline `y=732` |

**The icon-node is a formula.** A glyph of size *S* centered at `(cx, cy)` is `translate(cx − S/2, cy − S/2) scale(S/24)` with the icon's `stroke-width` set to `1.5 × 24/S` — so a 48px node scales by 2 and carries `stroke-width="0.75"`, and renders at the same 1.5 hairline as every stroke in the skill. Scaling without the compensation is the single most common way this type goes wrong: at 2× the icons come out at 3px and the diagram looks like clip art.

| Band | Offset from `cy` |
|---|---|
| Glyph | `−24` → `+24` |
| Name (Geist 12/600, centered) | baseline `+44` |
| Sublabel (mono 9, centered) | baseline `+60` |

**Reserve a 144 × 112 cell per icon-node.** Two nodes closer than 144 apart horizontally will collide at the labels, not at the glyphs — the glyph is 48 wide and the label is routinely three times that.

**Rings.** Radius 72 for a panel's main cycle, 44 for a ghost. Stations sit at the cardinal points (`θ = 0, 90, 180, 270`, measured from twelve o'clock, clockwise), which keeps every station centre on the grid. Arcs run station-to-station with a 12° gap at each end so the glyph is not struck through:

```
point(θ) = (cx + r·sinθ, cy − r·cosθ)
arc      = M point(θₖ+12) A r r 0 0 1 point(θₖ₊₁−12)
```

The hub glyph is 48px at the centre and its name sits at `cy + 44` — which clears a bottom station at `r = 72` by 13px and no more, so do not give the hub a sublabel. Ring captions replace per-station labels: a mono eyebrow above the ring at `cy − r − 26`, and one mono arrow-label below at `cy + r + 32` — far enough to clear a bottom station's glyph by 20px. Four labelled stations inside a 144px circle is unreadable at any size the diagram will actually be viewed at.

**Connectors obey SKILL.md §6 without exception.** Straight only when the endpoints share an axis; otherwise a rounded right-angle elbow at `r=8`. The two-way improvement cycle between a pair of nodes is **two separate horizontal arrows offset 24px vertically**, never one line with two arrowheads — a double-headed arrow says "these talk", where two lines say what each direction actually carries.

**Panels are drawn to the same frame.** Same width, same header treatment, same meter track, same baselines. Content density may differ — a broken mechanism usually *is* simpler than the one proposed to replace it — but a narrowed or faded before-panel is rhetoric, not drawing.

---

## Complexity budget

| Limit | Rule |
|---|---|
| Max panels | 2 — 3 only for before / interim / after, never as a timeline |
| Max icon-nodes per panel | 7 |
| Max rings per panel | 1 |
| Ring stations | 3–4 |
| Max ghost clusters | 1, in the after panel only |
| Max arrows per panel | 10, ring arcs included |
| Max consequence meters per panel | 2, sharing one unit |
| Cross-panel connectors | 0, always |
| Max accent elements | 1 **per diagram**, not per panel |

The node and arrow totals are a **zoned exemption** from SKILL.md §7's 9-node and 12-arrow limits, on the same terms as **ecosystem**, **platform stack**, and **capability map**: each panel is independently inside the limit, every node and every connector is inside a named panel, and nothing crosses the gutter, so the reader never holds both halves in working memory at once.

Exactly **one** accent element in the whole diagram, and it belongs on the **pivot** — the one node in the after panel that did not exist, or did not sit there, before. That is the discipline the type is worth having: if you cannot name a single pivot, you have not proposed a change, you have described two moods. One accent per panel is worse than none, because it says the two mechanisms are equally the point.

---

## Anti-patterns

- **A different cast in the two panels.** New actors on the right, missing ones on the left. The reader now has to work out whether the improvement came from the rewiring or from the three people you quietly added, and the honest answer is usually the latter. If the cast genuinely changes, that *is* the claim — make it in prose, or draw two separate diagrams and say so.
- **An arrow across the gutter.** It converts two competing mechanisms into one process, and once it is there every reviewer will ask what the arrow means. The answer is always "time passes", which is what the title already said.
- **Meters measuring different things.** *60% of time reviewing* on the left and *3 days to ship* on the right. Two units, no comparison, and the shape of the bars invents one anyway.
- **Ghosting in the before panel.** Nothing is superseded yet. A faded node on the left just reads as an element the author was unsure about.
- **Both panels drawn as straight chains.** If neither side has a cycle or a branch, there is no wiring to compare — the difference is a list of attributes. Write the table.
- **Boxing the icon-nodes.** A rounded rect around each glyph turns the panel into an architecture diagram with decorations, and drags in every expectation that comes with a box: ports, containment, layers. The glyph is the node.
- **Scaling icons without compensating the stroke.** 24px art at `scale(2)` renders 3px strokes beside 1.5px connectors, and the panel stops looking like the rest of the deck.
- **Emoji instead of glyphs.** They carry a platform's color, its rendering, and its tone, and none of the three are yours.
- **A third panel used as a timeline.** Before / during / after down a page is a **timeline** or a **process**. The third panel is legitimate only when an interim mechanism is genuinely being proposed as a distinct way of working.
- **An accent in each panel.** Two focal points, no focus — and the specific damage here is that the reader can no longer tell which side the diagram is arguing for.
- **A before panel starved to win the argument.** Fewer labels, thinner strokes, a shorter frame. Reviewers notice, and what they notice is the author's thumb on the scale.

## Examples

- `assets/example-contrast-panels.html` — minimal light
- `assets/example-contrast-panels-dark.html` — minimal dark
- `assets/example-contrast-panels-full.html` — full editorial
