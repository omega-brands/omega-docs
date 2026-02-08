# Canonical Diagram: Governed Execution Surfaces

## Purpose

This is the canonical diagram specification for the separation of powers between execution and governance interfaces. It can be rendered in Mermaid, Figma, SVG, or any diagramming tool.

It encodes separation of powers structurally — not artistically.

---

## Layer Order (top → bottom)

```
[ Workshop UI ]        [ Courtroom UI ]
        |                     |
        |                     |
        └────── Context ──────┘
                 |
           [ Keon Kernel ]
                 |
        [ Policy • Receipts • Evidence ]
```

---

## Layer Definitions

### Layer 1 — Interfaces (Top)

Two separate boxes, no overlap.

**Left: Workshop UI**

- Label: `Workshop (Execution Surface)`
- Subtext:
  - Propose execution
  - Observe state
  - Halt on governance
- Explicit ❌ icons next to:
  - Decide
  - Render Evidence
  - Export Proof

**Right: Courtroom UI**

- Label: `Courtroom (Governance Authority)`
- Subtext:
  - Decide outcomes
  - Require rationale
  - Render & export evidence
- Explicit ❌ icons next to:
  - Execute
  - Modify workflows

⚠️ **Important**: Do **not** connect Workshop → Courtroom directly with authority arrows.

---

### Layer 2 — Context Flow (Thin, neutral arrows)

- Arrow from Workshop → Kernel labeled: **"Execution Proposal"**
- Arrow from Courtroom → Kernel labeled: **"Governance Decision"**
- Optional dashed arrow between UIs labeled: **"Context only (no authority)"**

---

### Layer 3 — Kernel (Foundation)

Single wide box spanning beneath both UIs.

**Label:** `Governance Kernel (Keon)`

**Inside the box (stacked):**

- Policy Evaluation
- Gate Enforcement
- Receipt Generation
- Evidence Sealing
- Lineage Verification

**Styling rule:** Kernel box must visually outweigh UI boxes (thicker border, darker tone).

---

### Layer 4 — Artifacts (Bottom)

Connected **only** to Kernel.

Boxes:

- Policies
- Receipts
- Evidence Packs
- Seals & Hashes

---

## Caption

> Interfaces consume truth.
> The kernel enforces it.

---

## Diagram Caption Variants

Use these verbatim under rendered diagrams depending on context.

### Caption A (default, strongest)

> The kernel sits beneath all interfaces as the sole source of truth.
> Execution and governance are separated into distinct surfaces that cannot bypass or subsume one another.

### Caption B (flow-oriented)

> Execution proposes through the kernel.
> Governance decides through the kernel.
> Proof is emitted by the kernel — never by the interfaces.

### Caption C (gate emphasis)

> When governance is required, execution halts.
> Authority transfers visibly to the Courtroom, preserving accountability and auditability.

### Caption D (audit-centric)

> Policies, receipts, and evidence are enforced and recorded at the kernel boundary.
> User interfaces consume truth — they do not create it.

### Caption E (context without authority)

> Context may flow between interfaces.
> Authority never does.

