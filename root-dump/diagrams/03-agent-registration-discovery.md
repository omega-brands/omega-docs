# Agent Registration & Discovery Flow

```mermaid
sequenceDiagram
    participant Agent as New Agent
    participant Fed as Federation Core
    participant AR as Agent Registry
    participant MR as MCP Registry
    participant CS as Context Server
    participant PG as Praetorian Guard

    Note over Agent,PG: Agent Startup & Registration

    Agent->>Agent: Initialize with config
    Agent->>Agent: Generate Agent Passport (JWT)
    
    Agent->>Fed: POST {AGENT_REGISTRY_BASE}/register/agent
    Note right of Agent: {id, name, capabilities,<br/>endpoint, skills}
    
    Fed->>Fed: Validate Passport
    Fed->>Fed: Check manifest signature
    
    Fed->>AR: Store agent metadata
    AR->>AR: Persist to MongoDB
    AR-->>Fed: Registration confirmed
    
    Fed->>MR: Register MCP tools (if any)
    MR->>MR: Catalog tool capabilities
    MR-->>Fed: Tools registered
    
    Fed->>CS: Update context graph
    CS->>CS: Index agent capabilities
    CS-->>Fed: Context updated
    
    Fed->>PG: Add to health monitoring
    PG->>PG: Start heartbeat tracking
    PG-->>Fed: Monitoring active
    
    Fed-->>Agent: 201 Created + Agent ID
    
    Note over Agent,PG: Heartbeat & Health Monitoring

    loop Every 30 seconds
        Agent->>Fed: POST {AGENT_REGISTRY_BASE}/heartbeat/agent
        Fed->>AR: Update last_seen timestamp
        Fed->>PG: Reset failure counter
        Fed-->>Agent: 200 OK
    end

    Note over Agent,PG: Discovery & Capability Matching

    participant Client as Client Request
    
    Client->>Fed: GET /agents/discover?capability=code_generation
    Fed->>AR: Query by capability
    AR->>AR: Filter agents with skill
    AR-->>Fed: Matching agents list
    
    Fed->>Fed: Apply reputation scoring
    Fed->>Fed: Check circuit breaker status
    Fed->>Fed: Sort by performance metrics
    
    Fed-->>Client: Ranked agent list
    
    Note over Agent,PG: Task Routing

    Client->>Fed: POST /route {task, requirements}
    Fed->>CS: Get task context
    CS-->>Fed: Enriched context
    
    Fed->>AR: Find capable agents
    AR-->>Fed: Candidate list
    
    Fed->>Fed: Score candidates
    Note right of Fed: - Capability match<br/>- Current load<br/>- Historical performance<br/>- Reputation score
    
    Fed->>Agent: POST /execute {task, context}
    Agent->>Agent: Process task
    Agent-->>Fed: Task result
    
    Fed->>AR: Update agent metrics
    Fed->>PG: Report success
    Fed-->>Client: Return result

    Note over Agent,PG: Failure & Recovery

    PG->>PG: Detect missed heartbeat
    PG->>Fed: Agent health check failed
    Fed->>Fed: Activate circuit breaker
    Fed->>AR: Mark agent as unhealthy
    
    Fed->>PG: Trigger recovery protocol
    PG->>PG: Attempt agent restart
    
    alt Recovery Successful
        PG->>Agent: Restart container
        Agent->>Fed: Re-register
        Fed->>AR: Update status to healthy
        Fed->>Fed: Close circuit breaker
    else Recovery Failed
        PG->>Fed: Escalate to Genesis Protocol
        Fed->>Fed: Spawn replacement agent
    end

    Note over Agent,PG: Graceful Shutdown

    Agent->>Fed: DELETE /agents/{id}
    Fed->>AR: Remove from registry
    Fed->>MR: Unregister tools
    Fed->>CS: Update context graph
    Fed->>PG: Stop monitoring
    Fed-->>Agent: 204 No Content
```

## Registration Protocol

### 1. Agent Initialization
```json
{
  "agent_id": "code_generator_001",
  "name": "Code Generator",
  "description": "Transforms requirements into production code",
  "capabilities": ["code_generation", "architecture_design"],
  "skills": ["python", "typescript", "docker"],
  "endpoint": "http://code-generator:8080",
  "mcp_endpoint": "http://code-generator:8080/mcp",
  "version": "1.0.0",
  "passport": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 2. Discovery Query
```json
{
  "capabilities": ["code_generation"],
  "skills": ["python"],
  "min_reputation": 0.8,
  "max_results": 5
}
```

### 3. Discovery Response
```json
{
  "agents": [
    {
      "agent_id": "code_generator_001",
      "name": "Code Generator",
      "capabilities": ["code_generation", "architecture_design"],
      "reputation_score": 0.95,
      "avg_latency_ms": 150,
      "success_rate": 0.98,
      "current_load": 0.3,
      "endpoint": "http://code-generator:8080"
    }
  ],
  "total": 1,
  "query_time_ms": 12
}
```

## Health Monitoring

### Heartbeat Protocol
- **Interval**: 30 seconds
- **Timeout**: 90 seconds (3 missed heartbeats)
- **Payload**: `{"status": "healthy", "load": 0.3, "metrics": {...}}`

### Health States
- **HEALTHY**: Receiving regular heartbeats
- **DEGRADED**: Slow responses or high error rate
- **UNHEALTHY**: Missed heartbeats or circuit breaker open
- **OFFLINE**: Gracefully unregistered or terminated

### Circuit Breaker
- **Closed**: Normal operation
- **Open**: Too many failures, route around agent
- **Half-Open**: Testing recovery, limited traffic

