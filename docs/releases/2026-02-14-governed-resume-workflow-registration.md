# Governed Workflow Execution: Artifact Registration & Cryptographic Resume Input in OMEGA

Date: February 14, 2026  
Contract Version: 1  
Applies To: Federation Core, omega-sdk (TS/C#/Python), ForgePilot

## Executive Summary

OMEGA now supports:

- Deterministic workflow artifact registration
- Governed gate resume with validated input payload
- JCS-canonicalized input hashing
- Immutable resume ledger events
- SDK feature parity across TypeScript, C#, and Python

This release transitions OMEGA from a workflow orchestration engine into a governed execution substrate with deterministic lifecycle semantics.

## Why This Matters

Before this release:

- Resume operations were binary (approve/deny)
- Workflow definitions were invoked but not formally registered as content-addressable artifacts
- Resume inputs were not cryptographically hashed and ledgered

Now:

- Workflows are first-class artifacts
- Resume input is governed, validated, canonicalized, hashed, and persisted
- SDKs enforce identical lifecycle semantics across languages
- No side-channel state mutation is allowed

## Workflow Artifact Registration

Federation Core now exposes:

`POST /api/fc/workflows/register`

Registration properties:

- Accepts `workflow.yaml`, `prompts.poml`, and optional schemas
- Computes SHA-256 hashes of all artifacts
- Stores immutable artifact records
- Enforces idempotency on `(workflowId, version, artifactHashes)`

Result: workflows are deterministic, version-bound, content-addressable, and reproducible.

## Governed Resume with Input Payload

Federation Core now supports:

`POST /api/fc/runs/{run_id}:resume`

Request shape:

```json
{
  "runId": "string",
  "gateId": "string",
  "decision": "approve",
  "input": {}
}
```

Execution semantics:

- Schema validation
- JCS canonicalization
- SHA-256 `inputHash`
- Immutable ledger persistence in `gate_resume_events`
- Correlation and tenant binding

Validation failures fail closed with no partial state transition.

Ledger event introduced: `FC-GATE-003`.

## SDK Parity Across Languages

SDKs now support parity for:

- `workflows.register(...)`
- `workflows.resumeRun({ runId, gateId, decision, input })`

Parity guarantees:

- Correlation propagation
- Tenant binding
- Error mapping alignment
- Envelope consistency
- No cross-language drift

## ForgePilot Standardization

ForgePilot now runs in OMEGA-standard mode:

- SDK-only workflow execution
- Artifact-based workflow invocation
- Governed resume input
- `traceId` required
- `receiptRef` required on teaser success
- No bespoke Federation Core HTTP path

## Security and Governance Guarantees

- Resume input transitions are hash-bound and ledgered
- Workflow artifacts are content-addressable and immutable
- Fail-closed validation is enforced
- SDK lifecycle semantics remain consistent across languages

## FAQ

### What is governed workflow execution?

Governed workflow execution means workflow artifacts are versioned and hashed, and resume input is validated, canonicalized, and ledgered before execution continues.

### Why hash resume input?

To provide deterministic replay, forensic traceability, immutable lifecycle transitions, and mutation detection.

### What is JCS canonicalization?

JCS (JSON Canonicalization Scheme) serializes JSON deterministically before hashing so all SDKs compute the same hash.

### How is this different from traditional orchestration?

Traditional systems often accept mutable definitions and unhashed resume input. OMEGA registers artifacts, hashes resume input, persists immutable events, and fails closed on validation mismatch.

## Diagram: Workflow Artifact Lifecycle

```text
Authoring
   ↓
workflow.yaml + prompts.poml
   ↓
POST /workflows/register
   ↓
SHA-256 hash (artifact fingerprint)
   ↓
Immutable artifact store
   ↓
Workflow execution
   ↓
Trace + Receipt
```

Caption: Workflow definitions are content-addressable artifacts tied to execution fingerprints.

## Diagram: Governed Resume Input

```text
User Input
   ↓
resumeRun({ decision, input })
   ↓
Schema Validation
   ↓
JCS Canonicalization
   ↓
SHA-256 inputHash
   ↓
Ledger Event (FC-GATE-003)
   ↓
Workflow Continues
```

Caption: Resume transitions are governed lifecycle events, not UI continuations.

## Strategic Impact

This release enables provenance-first workflow lifecycle management across OMEGA consumers and removes ad-hoc resume semantics, SDK divergence, and execution ambiguity.

OMEGA implements governed workflow execution: artifact-registered, cryptographically hashed, and ledgered state transitions, powered by Keon.