# OMEGA

> **OMEGA (Orchestrated Multi-Expert Governed Agents)** is a governed execution platform for coordinating generative, deterministic, and policy-driven agents with built-in proof, privacy, and failure semantics.

---

## What OMEGA Is

A production-grade execution substrate for orchestrating multiple classes of agents across tools, workflows, and environments. [Learn more](docs/overview/what-is-omega.md)

---

## Why OMEGA Exists

To make delegation, automation, and agentic execution safe, explainable, and defensible by default. [Read the core concepts](docs/overview/core-concepts.md)

---

## The Classification Shift: From Orchestration to Governed Execution

OMEGA treats execution as something that must be provable, reconstructable, and constrained by design. [See the full analysis](docs/overview/classification-shift.md)

---

## Core Capabilities (High-Level)

Routing, execution, memory, workflow coordination, extensibility, and agent collaboration as first-class primitives. [Explore capabilities](docs/atlas/capabilities-index.md)

---

## Omega Core (Entity Lifecycle Governance)

OMEGA’s core enforces the **complete lifecycle** of autonomous digital entities — from creation through termination — with explicit authority, receipt-backed finality, and policy-driven automation.

- **Governed Birth** (PT-014 — Proven)
  - Entity creation requires explicit human or system authority
  - Receipt-bound birth events with fail-closed semantics
  - No entity exists without a governed genesis record
- **Governed Death** (PT-016 — Proven)
  - Revocation and termination produce immutable lineage
  - No death without birth (prevents phantom entities)
  - No double-death (prevents state corruption)
  - Two death modes: policy revocation vs system termination
  - Receipt chains link birth → death with no gaps
- **Governed Automation** (PT-017 — Proven)
  - Policies can trigger automatic revocation or termination
  - Severity gradation: RECOMMEND → AUTO_REVOKE → AUTO_TERMINATE
  - Human gate enforcement for irreversible actions
  - Cooldown periods prevent policy flapping
  - Full attribution: policy ID, version, automation flag, trigger events
  - Fail-closed: ambiguous cases default to NO_ACTION
- **Constitutional Guarantee**
  - Machines may act automatically — but always prove why, under whose authority, and with what limits
  - Every automated action is attributable, auditable, and reversible up to the point of execution
  - Receipt chains survive forensic reconstruction months or years later

---

## Receipts as a First-Class Primitive

Every execution can emit a deterministic receipt that proves what happened without exposing content. [Understand receipts](docs/atlas/functionality-summary.md)

---

## Privacy by Construction

Privacy is enforced structurally through schema, hashing, and policy boundaries rather than convention. [Best practices](docs/architecture/security/best-practices.md)

---

## Determinism, Replayability, and Proof Semantics

Same inputs produce the same proofs, enabling replay, verification, and auditability. [Proof semantics](docs/architecture/security/fortress.md)

---

## Where Keon Fits (Optional Governance Substrate)

Keon provides cryptographic governance and audit guarantees for OMEGA’s execution layer without changing its execution model. [Architecture overview](docs/architecture/overview.md)

---

## What This Unlocks

Once execution is provable, downstream systems become inevitable rather than aspirational. [See deliverables](docs/atlas/deliverables.md)

---

## Architecture at a Glance

A modular system composed of agents, execution engines, routing layers, memory systems, and optional governance substrates. [Full architecture](docs/architecture/overview.md)

---

## User Interfaces

OMEGA exposes execution through a deliberately constrained user interface called the **Workshop**.

The Workshop allows users to:
- discover workflows
- initiate governed execution
- observe run state and governance interruptions

It does **not** make decisions or render evidence.

- [Workshop UI (Execution Surface)](docs/ui/workshop-ui.md)
- [Governed Execution Diagram](docs/ui/governed-execution-diagram.md)
- [Auditor Walkthrough](docs/ui/auditor-walkthrough.md)
- [Why Not Open Source (Yet)](docs/ui/why-not-open-source.md)
- [Separation of Powers](docs/ui/separation-of-powers.md)

---

## Comparison

How does governed execution differ from conventional agent platforms? This framework evaluates systems on architecture, not claims.

- [Governed Systems vs. Conventional Agent Platforms](docs/comparison/governed-vs-agentic.md)

---

## Getting Started

OMEGA can be adopted incrementally, from local execution to governed multi-tenant workflows. [Quick start guide](docs/getting-started/quick-start.md)

---

## Explore the Full Surface Area

Detailed documentation covering the complete capability set, advanced systems, and deliverables. [Complete documentation](docs/atlas/documentation-complete.md)

---

## Design Principles

Restraint, clarity, credibility, and correctness over novelty and unchecked autonomy. [Advanced systems reference](docs/atlas/advanced-systems-reference.md)

---

## Proof Campaigns (What's Proven)

Every claim in OMEGA is backed by a sealed, tagged, independently verifiable proof campaign. These are not demos — they are **immutable evidence bundles** with SHA256-hashed manifests.

| Campaign | What It Proves | Status |
|----------|---------------|--------|
| **PT-003** | Agent Registry & Capability Routing | ✅ Proven |
| **PT-004** | Workflow Orchestration Execution Spine | ✅ Proven |
| **PT-005** | Explicit GATE_REQUIRED Ergonomics (Human-in-the-Loop) | ✅ Proven |
| **PT-013** | Multi-Titan Collaboration under FC Governance | ✅ Proven |
| **PT-014** | Genesis under Human-Governed Execution (Birth) | ✅ Proven |
| **PT-016** | Governed Revocation & Death Semantics (Death) | ✅ Proven |
| **PT-017** | Revocation Policy Automation (Automated Governance) | ✅ Proven |

> **Birth, Death, and Automation are all governed, attributed, and provable.**

Full proof artifacts, harness code, and evidence bundles: [OMEGA Proof Campaign Status](https://github.com/m0r6aN/omega-docs/blob/main/REPORT/PROOFS/PROOF_CAMPAIGN_STATUS.md)

---

## Status and Maturity

An actively developed, production-tested system with **7 sealed proof campaigns** covering the full governance lifecycle. [Documentation status](docs/atlas/documentation-complete.md)

---

## Roadmap Signal (High-Level)

Focused on deepening proof semantics, federation flexibility, and system evolvability. [Roadmap details](docs/atlas/final-additions-summary.md)

---

## Who This Is For

Teams building systems where correctness, explainability, and control matter. [Start here](docs/atlas/start-here.md)

---

## Who This Is Not For

Toy agents, prompt demos, or systems optimized solely for novelty.

---

## Contributing and Collaboration

Built to be extended, audited, and evolved through disciplined collaboration.

---

## Receipts

Every execution produces a deterministic receipt. Here's a concrete example:

```json
{
  "event": "email.action.executed",
  "workflowId": "wf_personal_signal_firewall",
  "stepId": "act.reply_decline",
  "status": "success",
  "correlationId": "corr_...",
  "inputHash": "sha256:...",
  "outputHash": "sha256:...",
  "receiptHash": "sha256:...",
  "meta": { "source": "gmail", "fromDomain": "recruiterco.com", "reasonCodes": ["stack_mismatch"] }
}
```


