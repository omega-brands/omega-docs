# 🧠 OMEGA Memory Resource

**MCP-Enabled Semantic Memory Storage and Retrieval**

## Overview

The Memory Resource is an MCP (Model Context Protocol) Resource that provides semantic memory storage and retrieval capabilities with reinforcement learning. It exposes memory operations as a standardized MCP resource, making it accessible to all agents and tools in the OMEGA ecosystem.

## Architecture

- **Type**: MCP Resource (not a Tool)
- **Base Class**: `OmegaResource` from `tools/base_resource.py`
- **Backend**: Memory API service (port 9227)
- **Port**: 9209 (standard OMEGA resource port)
- **Access Level**: Public

## Why a Resource Instead of a Tool?

Resources in MCP represent **data access patterns**, while Tools represent **operations/actions**. Memory is fundamentally about:
- Storing and retrieving data
- Providing access to persistent information
- Serving as a knowledge base

This aligns perfectly with the Resource pattern, similar to how prompts, policies, and templates are exposed as resources.

## Features

- ✅ **Deduplication** - Automatic deduplication via source_hash
- ✅ **Semantic Search** - Vector similarity search with Qdrant
- ✅ **Reinforcement Learning** - Feedback-based weight adjustment
- ✅ **TTL Management** - Four-tier lifecycle (short/standard/long/eternal)
- ✅ **Multi-tenant Support** - Source and tag-based filtering
- ✅ **MCP Compliant** - Auto-registers with MCP Registry

## Endpoints

### Standard MCP Resource Endpoint

```
GET /resources/memory
```

Returns metadata about the memory resource and available operations.

### Memory Operations

#### Store Memory
```
POST /memory/store
```

**Payload:**
```json
{
  "content": "The memory content to store",
  "source": "user",
  "tags": ["important", "project-x"],
  "ttl_tier": "standard",
  "metadata": {},
  "deduplicate": true
}
```

#### Query Memory
```
POST /memory/query
```

**Payload:**
```json
{
  "query": "search query",
  "top_k": 5,
  "min_similarity": 0.7,
  "tags": ["project-x"],
  "source": "user"
}
```

#### Provide Feedback
```
POST /memory/feedback
```

**Payload:**
```json
{
  "shard_id": "memory-shard-id",
  "feedback": "positive",
  "boost_amount": 0.1
}
```

#### Get Specific Memory
```
GET /memory/get/{shard_id}
```

## Usage

### Running the Resource

```bash
python -m resources.memory.resource
```

Or via uvicorn:

```bash
uvicorn resources.memory.resource:MemoryResource.app --host 0.0.0.0 --port 9209
```

### Using from Python

```python
from resources.memory import MemoryResource

# Create the resource
memory = MemoryResource()

# Run the server
import uvicorn
uvicorn.run(memory.app, host="0.0.0.0", port=9209)
```

### Using via HTTP

```bash
# Store a memory
curl -X POST http://localhost:9209/memory/store \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Important project decision",
    "source": "user",
    "tags": ["decision", "project-alpha"]
  }'

# Query memories
curl -X POST http://localhost:9209/memory/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "project decisions",
    "top_k": 5
  }'

# Provide feedback
curl -X POST http://localhost:9209/memory/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "shard_id": "abc123",
    "feedback": "positive"
  }'
```

## Configuration

The Memory Resource uses the centralized config service:

- `MEMORY_API_URL` - Backend Memory API URL (default: `http://memory-api:9227`)
- `MCP_REGISTRY_URL` - MCP Registry URL for auto-registration

## Integration with OMEGA Ecosystem

The Memory Resource automatically:
1. Registers with the MCP Registry on startup
2. Exposes standard MCP Resource endpoints
3. Provides health and metadata endpoints
4. Uses OMEGA's centralized configuration
5. Follows OMEGA doctrine for resources

## TTL Tiers

- **short** - Ephemeral memories (hours)
- **standard** - Regular memories (days)
- **long** - Important memories (weeks/months)
- **eternal** - Permanent memories (never expire)

## Reinforcement Learning

Memories can be reinforced through feedback:
- **Positive feedback** - Increases weight_boost (makes memory more relevant)
- **Negative feedback** - Decreases weight_boost (makes memory less relevant)

The final score in search results = `similarity * weight_boost`

## This is the way.

🔱 **OMEGA Pantheon** - AugmentTitan, The Architect

