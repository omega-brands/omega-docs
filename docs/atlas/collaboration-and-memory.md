# OMEGA Collaboration & Physics-Based Memory Systems

## 🎭 Whiteboard Session Protocol (CANON — ENFORCED)

**Status**: CANON — Enforced at runtime  
**Scope**: Multi-agent collaboration, moderation, and conversational flow  
**Applies To**: Director, Moderator, Orchestrator, Context Server, Titans

### Core Philosophy

> **Shared state is authoritative. Conversation history is not.**

The Whiteboard Session Protocol prevents verbosity, context bloat, and simultaneous monologues by enforcing:
- **State-based collaboration** (whiteboard over transcript)
- **Disciplined turn-taking** (one speaker at a time)
- **Timeboxed responses** (3-5 sentences, ~100 tokens max)
- **Strict response contracts** (format validation with repair retry)
- **Bounded context windows** (Baton Context Model)

### Conversation Moves

1. **IDEATION** - Raw idea extraction (parallel, isolated, fixed-count output)
2. **CONSOLIDATION** - Create shared whiteboard with stable IDs (idea.01, idea.02, etc.)
3. **DISCUSSION** - Explore/refine ideas collaboratively (turn-based, must reference board item)
4. **POSITIONING** - Force clarity of stance (one sentence per Titan: option + reason)
5. **HANDOFF** - Produce execution-ready directive (no tools, no side effects)

### Key Components

**The Director**
- Non-generative control component
- Selects conversation move
- Configures response_contract, context_policy, token_budget
- Outputs JSON only

**The Moderator**
- Flow authority and protocol enforcer
- Sole writer of Whiteboard State
- Enforces turn order and timeboxing
- Controls phase transitions (SOLE AUTHORITY)
- Broadcasts results ONCE per round

**The Whiteboard**
- Authoritative shared state (NOT conversation transcript)
- Structured representation of ideas and decisions
- Moderator-only writes; Titans propose updates
- Stable ID generation (idea.01, point.02, decision.03)
- Phase history for audit trail

### Context Model (Baton Context)

Each Titan receives ONLY:
1. Whiteboard State (authoritative)
2. Focus item (required for DISCUSSION/DECISION)
3. Immediate previous response (verbatim baton)
4. Optional prior summary (compressed), if needed

**NOT included**: Full transcript history, conversation archives

### Decision Thresholds

- **Default**: Simple majority
- **Exception**: Any Titan may flag `critical_risk=true`
- **If flagged**: Moderator halts decision for human review

---

## 🎯 Debate Protocol

**Formal debate mechanics** with structured argumentation:

- **Positioning Phase** - One sentence per Titan (preferred option + primary reason)
- **Consensus Voting** - Reputation-weighted voting with 3/4 Titan threshold
- **Debate Synthesis** - Automated synthesis of debate outcomes into decisions
- **Conflict Resolution** - Disputes resolved via voting and arbitration
- **Swarm Consensus** - Distributed consensus protocol for collective decisions

---

## 🧬 CollaboratorMixin (Swarm Intelligence Gene)

**Genetic implant** for any BaseAgent enabling swarm participation:

- **Self-Selecting Task Relevance** - Agents detect task relevance via `is_task_relevant()`
- **Decentralized Event-Driven Collaboration** - Redis streams-based task consumption
- **Concurrent Processing** - Intelligent load management with backpressure
- **Orphaned Task Recovery** - Automatic claiming of abandoned tasks
- **Performance-Based Adaptive Behavior** - Load balancing based on agent performance

---

## 🌌 Physics-Based Memory: Six-Force Attraction Model

Memory retrieval is governed by **six attraction forces**:

1. **Semantic Mass** (0.35 weight) - Vector similarity to query
2. **Recency Inertia** (0.20 weight) - Time-based decay (7-day half-life)
3. **Access Frequency** (0.15 weight) - How often accessed (capped at 10/hour)
4. **Identity Alignment** (0.10 weight) - Alignment with Titan identity
5. **Mission Alignment** (0.10 weight) - Alignment with current task
6. **Lineage Compatibility** (0.10 weight) - Genealogical relationship to context

### Gravity Well Principle

High-mass memories (identity-defining events, core victories, foundational failures) form **persistent gravity wells**:
- Remain in orbit even when not explicitly invoked
- Decay significantly slower than peripheral memories
- Titans "enter orbit" around memories whose attraction exceeds threshold
- Routing is emergent, not explicit

### Memory Strata (Three Layers)

1. **Chronicle** - Personal memory (individual agent experiences)
2. **Doctrine** - Shared knowledge (collective swarm protocols)
3. **Akashic** - Universal knowledge (system-wide foundational principles)

Hard boundaries between strata; different attraction dynamics per layer.

### Memory Law & Enforcement

- **MRF (Memory Routing Firewall)** - Pre-conscious enforcement layer
- **Fail-Closed Architecture** - Deny on uncertainty
- **Cryptographic Exclusion** - Unauthorized shards blocked
- **Owner-Based Access Control** - Restricted by ownership/permissions
- **Immutable Audit Trail** - No decision without logging

### Eternal Memory Architecture

- **Semantic Chunking** - 7 shard types per conversation
- **GPU-Accelerated Embeddings** - 384-dimensional vectors
- **Dual Storage** - Qdrant vectors + MongoDB metadata
- **Async Polling** - 60-second polling for new events
- **Vector Retrieval** - Semantic search for context injection

---

## 🔗 Real-Time Collaboration

- **WebSocket Collaboration** - Real-time updates between frontend and Federation Core
- **Live Debate Streaming** - WebSocket streaming of multi-agent debates
- **Pantheon Collaboration** - Real multi-agent workflows (NOT simulation)
- **Titan Orchestration** - Complex multi-step business processes via `Pantheon.collaborate()`


