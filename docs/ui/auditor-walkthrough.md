# Governed Execution Walkthrough (UI Perspective)

This walkthrough is designed for auditors, risk teams, security reviewers, and enterprise buyers. No code. No demos. Just the governance model as experienced through the user interfaces.

---

## Step 1 — Execution Is Proposed (Workshop)

An operator initiates a workflow from the **Workshop UI**.

What the UI does:
- Submits a proposal to the kernel
- Displays run state
- Shows no decision controls

What it cannot do:
- Override policy
- Approve outcomes
- Render evidence

**Audit implication:** Execution intent is recorded without granting authority.

---

## Step 2 — Governance Interrupts (Gate)

If policy requires human review:
- Execution halts automatically
- Workshop displays a **GATE_REQUIRED** state
- A governance case ID is issued

No workaround exists at the UI level.

**Audit implication:** Human review is mandatory and unavoidable.

---

## Step 3 — Decision Is Made (Courtroom)

A human reviewer opens the case in the **Courtroom UI**.

The UI enforces:
- Explicit rationale
- Policy version binding
- Lineage verification

The reviewer may:
- Accept
- Reject

**Audit implication:** Human intent is captured, contextualized, and bound to policy.

---

## Step 4 — Proof Is Emitted (Kernel)

Upon decision:
- The kernel records the outcome
- A receipt is generated
- An evidence pack is sealed

Evidence is viewable **only** in the Courtroom.

**Audit implication:** Proof is immutable, verifiable, and system-generated.

---

## Step 5 — Execution Resumes or Terminates

The Workshop UI updates:
- Execution continues **only** if approved
- Or terminates with recorded reason

The Workshop never handles proof artifacts.

**Audit implication:** Execution reflects governance outcomes without absorbing authority.

---

## Final Auditor Assertion

> No interface in this system can both act and justify its actions.
> This preserves accountability, traceability, and legal defensibility.

