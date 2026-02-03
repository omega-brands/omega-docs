# Gateway Ingress and Portless Identities

Standardize public identities and derived endpoints using base URLs and a local gateway that mirrors Azure Application Gateway.

## Why
- Stable, portless public identities (swap base only when moving to Azure)
- Derived endpoints from base (no more hardcoded register/heartbeat URLs)
- Local nginx gateway emulates Azure AGW path-based routing

## Keys
- AGENT_REGISTRY_BASE: Base for agent registration/heartbeat
- AGENT_PUBLIC_BASE: Preferred public identity for agents
- TITAN_PUBLIC_BASE: Preferred public identity for Titans (falls back to AGENT_PUBLIC_BASE)

## Behavior
- Register: {AGENT_REGISTRY_BASE}/register/agent
- Heartbeat: {AGENT_REGISTRY_BASE}/heartbeat/agent
- Public Identity: TITAN_PUBLIC_BASE or AGENT_PUBLIC_BASE (no ports)

## Local Gateway
- External: http://localhost:8080/
- Internal DNS: http://gateway/
- Paths:
  - /api/core/agent_registry → Agent Registry
  - /api/titans/{titan} → Titan services

```mermaid
graph TB
  GW[nginx Gateway\nhttp://localhost:8080/\nhttp://gateway/]
  AR[Agent Registry]
  CLAUDE[ClaudeTitan]
  GEMINI[GeminiTitan]

  GW -- /api/core/agent_registry --> AR

## Nginx Path Rules (excerpt)

```nginx
server {
  listen 80;
  server_name gateway;

  # Core services
  location /api/core/agent_registry/ {
    proxy_pass http://agent_registry:9401/;
  }

  # Titans
  location /api/titans/claude/ {
    proxy_pass http://claude_titan:9600/;
  }
  location /api/titans/gemini/ {
    proxy_pass http://gemini_titan:9601/;
  }
  # Example catch-all for titans with upstream map
  # location ~ ^/api/titans/(.+?)/ {
  #   set $titan $1;
  #   proxy_pass http://$titan/; # requires upstream names to match DNS
  # }
}
```

  GW -- /api/titans/claude --> CLAUDE
  GW -- /api/titans/gemini --> GEMINI

  subgraph BaseAgent
    BA[BaseAgent]
    BA -- derives --> R[{AGENT_REGISTRY_BASE}/register/agent]
    BA -- derives --> H[{AGENT_REGISTRY_BASE}/heartbeat/agent]
    BA -- identity --> P[{AGENT_PUBLIC_BASE} or {TITAN_PUBLIC_BASE}]
  end
```

## Verify
```bash
# Compose config sanity
docker compose -f omega-core/docker-compose.yml config

# Bring up gateway + registry + titans
docker compose -f omega-core/docker-compose.yml up -d --build gateway agent_registry claude_titan gemini_titan gpt_titan grok_titan

# Health via gateway
curl -sf http://localhost:8080/api/core/agent_registry/health
curl -sf http://localhost:8080/api/titans/claude/health
curl -sf http://localhost:8080/api/titans/gemini/health

# Logs
docker logs -f agent_registry | grep -E "TITAN REGISTERED|heartbeat"
docker logs -f claude_titan | grep -E "Registering with URL|heartbeat"
```

## Flip-the-switch (optional)
Set AGENT_REGISTRY_BASE=http://gateway/api/core/agent_registry for all services to route all internal calls via gateway (perfect Azure parity).



---

## See also
- Developer → Configuration → [Identities and Routing](/docs/developer/config/identities-and-routing)
- Developer → Configuration → [Environment Examples (.env)](/docs/developer/config/env-examples)
- Operations → [Deployment Guide](/docs/operations/deployment)
