# O.M.E.G.A. — Orchestrated Multi-Expert Gen Agents

Production-grade, containerized, MCP-native, A2A-aware multi-agent framework for real work.

## What’s new (v1.0.0)

- Agents standardized: env-driven registration, health, metrics (no hardcodes), typed inputs/outputs, connection-safe HTTP/Redis clients.
- Adapt “Ramsay loops” baked into key agents for iterative self-critique & improvement.
- Resilience hooks documented: **Praetorian Guard** (Survive) + **Genesis** (Procreate & Trigger).
- Docs synced to current env and infrastructure.

## Core Principles

- **Routing Law, Memory Law, Planning Law** (Doctrinal guardrails for routing, memory, and planning).
- **Survive → Adapt → Procreate** lifecycle: Praetorian (Survive), Agents (Adapt), Genesis (Procreate).

## Environment Variables (selected)
>
> Only names are listed here; set values via your secrets manager or `.env`.

| Key | Purpose |
|---|---|
| `FEDERATION_CORE_URL`, `FEDERATION_WS_URL`, `AGENT_REGISTRY_URL`, `AGENT_HEARTBEAT_URL` | Control plane + agent registry endpoints (service DNS in Docker) :contentReference[oaicite:0]{index=0} |
| `CONTEXT_SERVER_URL` | Oracle/Context Server base URL :contentReference[oaicite:1]{index=1} |
| `PROMETHEUS_URL` | Metrics sink (Prometheus) :contentReference[oaicite:2]{index=2} |
| `REDIS_URL` / `REDIS_HOST`/`REDIS_PORT` | Cache, queues, events :contentReference[oaicite:3]{index=3} |
| `MONGODB_URI` | Memory provider (Mongo) :contentReference[oaicite:4]{index=4} |
| `PRAETORIAN_PORT`, `PRAETORIAN_MCP_PORT`, `PRAETORIAN_AUTO_START` | Praetorian Guard config :contentReference[oaicite:5]{index=5} |
| `HEARTBEAT_INTERVAL`, `HEARTBEAT_EXPIRY` | Agent heartbeat cadence & expiry :contentReference[oaicite:6]{index=6} |
| `REDIS_CHANNEL_*` (e.g., `REDIS_CHANNEL_FEEDBACK`) | Federation channels (feedback, events, orchestration) :contentReference[oaicite:7]{index=7} |

> Keep **API keys** out of git. (They’re present in the example `.env` you shared—rotate them and move to a secrets store ASAP.) :contentReference[oaicite:8]{index=8}

## Agent Standards (applies to all agents)

- **Versioning**: `__version__ = "1.0.0"`.
- **No URL hardcodes**: read service bases from env; use the BaseAgent HTTP client.
- **Health & Metrics**: enable via env, export Prometheus format; no ad-hoc prints.
- **Typed I/O**: Pydantic models for tools + envelope payloads.
- **Feedback loops**: integrate an Adapt loop (Ramsay loop) for self-critique & improvement.
- **Registration**: auto-register + heartbeat using env registry endpoints.

## Resilience Hooks

- **Praetorian Guard** — monitors Redis/Mongo/Federation/Context, performs remediation, and exposes control tools (start/stop/force_check). Reads targets from env; no hardcoded paths. :contentReference[oaicite:9]{index=9}
- **Genesis Protocol** — auto-spawn/evolve agents/tools on validated triggers; see “Genesis” below.

# OMEGA Core — Agent Standards (v1.0.0)

## Must-Haves for Every Agent

1. **Settings** extend `AgentSettings`, with ports/flags from env:
   - Example: `RESEARCH_PORT`, `RESEARCH_MCP_PORT`, `HEARTBEAT_INTERVAL`, `PROMETHEUS_URL`.
2. **Registration/Heartbeat**: use registry env URLs (no inline URL literals). :contentReference[oaicite:10]{index=10}
3. **Health + Metrics**: `/health`, `/metrics` exposed; toggled by env.
4. **Typed Tools**: Define request/response Pydantic models for MCP tools.
5. **No URL building**: derive base via env; path constants configurable (e.g., `CONTEXT_CONTEXT_PATH=/context`). :contentReference[oaicite:11]{index=11}
6. **Adapt (Ramsay loop)**: iterative self-critique → improve → stop when quality ≥ threshold or max rounds.
7. **Logging**: centralized logger, structured logs; no print.

## Feedback (Adapt) Loop

- Use a `ramsay_loop(generate, critique)` pattern to improve outputs.
- Emit feedback events to `REDIS_CHANNEL_FEEDBACK` when present. :contentReference[oaicite:12]{index=12}

## Tests & Coverage

- Place tests in `core/tests/agents/<agent_name>/`.
- Target **≥80% coverage** via unit tests on each tool method + loop logic.
- Run: `pytest --maxfail=1 --disable-warnings -q`.
# omega-core
