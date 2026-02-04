# 🔥 Cognitive Forge - The Divine Routing Layer

## Overview

**Cognitive Forge** is the provider-agnostic inference routing hub of the OMEGA Pantheon. It intelligently routes inference requests to the optimal Titan based on capability matching, performance metrics, and task requirements.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    INCOMING REQUEST                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
         ┌─────────────────────────────┐
         │   COGNITIVE FORGE (9409)    │ ◄── Provider-agnostic entry point
         │  "What needs to be done?"   │
         └──────────┬──────────────────┘
                    │
                    ▼
         ┌─────────────────────────────┐
         │ CAPABILITY MATCHER (9008)   │ ◄── "Who can do it best?"
         │  Semantic Agent Selection   │
         └──────────┬──────────────────┘
                    │
                    ▼
         ┌─────────────────────────────┐
         │    SELECTED TITAN           │ ◄── Execution
         │  (GPT/Claude/Gemini/Grok)   │
         └─────────────────────────────┘
```

## Features

### 🎯 Intelligent Routing
- **Semantic Capability Matching**: Uses CapabilityMatcher to analyze query intent
- **Performance-Based Selection**: Routes to healthy, high-performing Titans
- **Requirement Matching**: Matches specific capability requirements to Titan strengths

### 🔌 Provider Flexibility
- **Multi-Provider Support**: GPT, Claude, Gemini, Grok
- **Forced Provider**: Option to force specific provider when needed
- **Automatic Failover**: Falls back to alternative Titans if primary is unavailable

### 🛡️ Production Ready
- **Circuit Breaker Integration**: Avoids unhealthy Titans
- **Timeout Protection**: 60s timeout on Titan invocations
- **Error Handling**: Comprehensive error handling and logging
- **Health Monitoring**: Built-in health checks

## API Endpoints

### POST `/forge/inference`

Main inference routing endpoint.

**Request:**
```json
{
  "query": "Create a strategic plan for scaling microservices",
  "requirements": ["strategic_planning", "synthesis"],
  "provider": null,  // Optional: force specific provider
  "temperature": 0.7,  // Optional
  "max_tokens": 4000,  // Optional
  "metadata": {}  // Optional
}
```

**Response:**
```json
{
  "request_id": "forge_1234567890",
  "query": "Create a strategic plan...",
  "selected_titan": "claude_titan",
  "confidence_score": 0.95,
  "result": {
    "success": true,
    "titan": "claude_titan",
    "result": "..."
  },
  "processing_time": 2.34,
  "timestamp": "2025-02-03T12:34:56Z",
  "forged": true
}
```

### POST `/forge/invoke`

Legacy endpoint for backward compatibility.

**Request:**
```json
{
  "query": "Your query here",
  "provider": "gpt",  // Optional
  "metadata": {}
}
```

## Usage Examples

### Python

```python
import httpx
import asyncio

async def forge_inference(query: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:9409/forge/inference",
            json={
                "query": query,
                "requirements": ["strategic_planning"]
            }
        )
        return response.json()

result = asyncio.run(forge_inference(
    "Design a resilient microservices architecture"
))
print(f"Routed to: {result['selected_titan']}")
```

### cURL

```bash
curl -X POST http://localhost:9409/forge/inference \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Find security vulnerabilities in this code",
    "requirements": ["security", "validation"]
  }'
```

### Force Specific Provider

```bash
curl -X POST http://localhost:9409/forge/inference \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Generate creative brand concepts",
    "provider": "gpt"
  }'
```

## Titan Selection Logic

### Automatic Selection

When no provider is specified, Cognitive Forge uses CapabilityMatcher to select the optimal Titan:

1. **Query Analysis**: Analyzes query text and requirements
2. **Capability Scoring**: Scores each Titan's capabilities against requirements
3. **Performance Weighting**: Factors in Titan health and performance history
4. **Best Match Selection**: Selects highest-scoring available Titan

### Scoring Weights (CapabilityMatcher)

- **Name Match**: 40% - Direct capability name matches
- **Description Match**: 30% - Semantic description matching
- **Confidence**: 20% - Titan's confidence in capability
- **Availability**: 10% - Titan health and performance

### Titan Specializations

- **ClaudeTitan** (9100): Strategic planning, synthesis, complex reasoning
- **GPTTitan** (9104): Creative ideation, branding, innovation
- **GeminiTitan** (9102): Security, validation, compliance, technical analysis
- **GrokTitan** (9106): Chaos engineering, stress testing, failure analysis

## Deployment

### Docker Compose

```yaml
cognitive_forge:
  build: ./services/cognitive_forge
  ports: ["9409:9409"]
  depends_on:
    - redis
    - capability_matcher
  environment:
    - REDIS_URL=redis://redis:6379/0
```

### Standalone

```bash
cd services/cognitive_forge
python -m services.cognitive_forge.service
```

## Testing

Run the integration test suite:

```bash
python tests/test_cognitive_forge_integration.py
```

This will test:
- Service health checks
- Capability matching
- Inference routing for different query types
- Forced provider selection
- Error handling

## Configuration

### Environment Variables

- `PORT`: Service port (default: 9409)
- `REDIS_URL`: Redis connection URL
- `AGENT_REGISTRY_URL`: Agent Registry URL
- `FEDERATION_CORE_URL`: Federation Core URL

### Titan Ports

Configured in `CognitiveForge.TITAN_PORTS`:
- claude_titan: 9100
- gpt_titan: 9104
- gemini_titan: 9102
- grok_titan: 9106

## Integration with Federation

Cognitive Forge can be integrated into Federation Core for automatic routing:

```python
# In Federation Core
async def route_inference(query: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://cognitive_forge:9409/forge/inference",
            json={"query": query}
        )
        return response.json()
```

## Monitoring

### Health Check

```bash
curl http://localhost:9409/health
```

### Metrics

Cognitive Forge logs:
- Request routing decisions
- Titan selection reasoning
- Performance metrics
- Error rates

## Future Enhancements

- [ ] **Cost Optimization**: Route to cheapest capable Titan
- [ ] **Load Balancing**: Distribute load across multiple Titans
- [ ] **Caching**: Cache frequent queries
- [ ] **A/B Testing**: Compare Titan performance
- [ ] **Custom Routing Rules**: User-defined routing logic
- [ ] **Streaming Support**: Stream responses from Titans

## Related Components

- **CapabilityMatcher** (`agents/capability_matcher`): Intelligent agent selection
- **InterTitanRouter** (`routing/inter_titan_router.py`): Performance-based routing
- **BaseTitan** (`titans/base_titan.py`): Titan base class with `/execute_task` endpoint

## Support

For issues or questions:
- Check logs: `docker logs cognitive_forge`
- Test health: `curl http://localhost:9409/health`
- Run tests: `python tests/test_cognitive_forge_integration.py`

---

**Status**: ✅ Production Ready
**Version**: 1.0.0
**Doctrine**: Service (Where/How)
**Genesis-Ready**: Yes
**MCP-Enabled**: Yes

