# Workshop UI (omega-flow)

## Mental Model

**The Workshop is where execution is proposed and observed — never governed.**

The Workshop UI is a read-only execution surface for:
- discovering workflows
- initiating governed runs
- monitoring execution state
- observing governance interruptions

It cannot:
- decide outcomes
- modify policies
- render or export evidence
- bypass governance gates

These constraints are not omissions. They are enforced architectural invariants.

---

## What the Workshop Is Allowed to Do

- Discover available workflows exposed by the kernel
- Create execution runs under governance
- Monitor run state transitions
- Halt visibly on governance gates (`GATE_REQUIRED`)
- Deep-link into governance when human decisions are required
- Display *metadata only* for evidence presence (hashes, seals)

---

## What the Workshop Is Forbidden From Doing

- Rendering evidence artifacts
- Exporting receipts
- Accepting or rejecting decisions
- Editing policy bindings
- Executing without kernel verification

If the Workshop cannot verify required hashes or lineage, it fails closed.

---

## Core Screens

### Workflow Catalog

![Workflow Catalog Screenshot](../assets/ui/workshop-workflows.png)

**Caption**
> The workflow catalog presents executable capabilities without implying authority.
> Availability does not mean permission — execution is always mediated by governance.

---

### Run Monitor (Active Execution)

![Run Monitor Screenshot](../assets/ui/workshop-run-monitor.png)

**Caption**
> The run monitor shows execution as an observable process, not a controllable one.
> State transitions are reported by the kernel and cannot be overridden here.

---

### Governance Gate Banner

![Gate Required Screenshot](../assets/ui/workshop-gate-banner.png)

**Caption**
> When governance intervention is required, execution halts visibly and unambiguously.
> The Workshop provides context and a case reference — then yields authority.

---

## Evidence Awareness (Without Access)

The Workshop may display:
- Evidence Pack present / absent
- Manifest hash
- Seal hash
- Policy lineage hash

It may **never** display or export artifacts.

**Rationale:**
Allowing evidence rendering here would collapse execution and governance into a single surface, breaking auditability and separation of powers.

---

## Architectural Invariant

> **omega-flow proposes and observes.
> It never decides.
> It never proves.**

This invariant is enforced in code, UX, and failure modes.

