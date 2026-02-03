# Classification Shift: From Orchestration to Governed Execution

Execution at scale is no longer just about getting steps to run in the right order. OMEGA demands that every action be provable, auditable, and confined to the bounded context that governance policies define. That conceptual evolution is what we call the **classification shift**: an explicit move from viewing execution as orchestration (a series of calls and handoffs) to seeing it as **governed execution** (a designed, observable, and enforceable workflow).

## Orchestration as choreography
Orchestration assumes trust in the actors, implicit handoffs between systems, and a focus on sequencing: run job A, then job B, and so on. While that approach works for tightly coupled internal services, it leaves gaps when humans, external agents, or regulatory requirements enter the picture. The lack of formal verification, replayability, or constraint enforcement can lead to inconsistent outcomes and opaque decision-making.

## Governed execution as designed intent
Governed execution layers explicit policies, proof obligations, and observability onto every transition. Rather than just wiring steps together, teams define what each step is allowed to do, how it reports state, and how downstream systems can rely on its output. This makes execution **verifiable** (you can see what happened), **reconstructable** (you can replay or audit the flow), and **constrained** (it cannot deviate outside agreed boundaries).

## What changes for practitioners
Shifting to governed execution means engineers and operators collaborate on policy definitions as much as on pipelines. Workflows become more declarative: instead of scripting each exception path, you classify the role the workflow plays, align it with governance guardrails, and trust the runtime to enforce them. Observability becomes a governance tool—every decision point emits metadata that answers, "Why did this action run, and why was it allowed?"

## Where to go next
- Use this overview whenever you need to explain *why* we care about governance over orchestration.
- For the advanced, internal view of *what* changed in the atlas implementation, see the internal reference at `docs/atlas/final-additions-summary.md`.

For a detailed summary of the concrete changes that enabled this shift, see the internal reference in the atlas at `docs/atlas/final-additions-summary.md`.
