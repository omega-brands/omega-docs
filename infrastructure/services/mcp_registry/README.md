# OMEGA MCP Registry Service v1.0

## Sacred Keeper of Tools and Servers

The MCP Registry is the central authority for all Model Context Protocol (MCP) tools and servers in the OMEGA ecosystem. It manages registration, lifecycle, discovery, and health monitoring of MCP components.

## 🔱 Sacred Responsibilities

- **Tool Registration**: Register and track all MCP tools in the ecosystem
- **Server Management**: Manage lifecycle of remote MCP servers (STDIO, HTTP, SSE, WebSocket)
- **Health Monitoring**: Continuous health checks with automatic recovery
- **Discovery Service**: Make capabilities discoverable to the Federation
- **Federation Integration**: Expose tools and servers to Titans and Agents

## 🚀 Quick Start

### Using Docker Compose (Recommended)

```bash
# Start the service with dependencies
docker-compose up -d

# View logs
docker-compose logs -f mcp-registry

# Stop the service
docker-compose down
```

### Direct Python Execution

```bash
# Install dependencies
pip install -r requirements.txt

# Set required environment variables
export REDIS_URL=redis://localhost:6379
export MONGODB_URI=mongodb://localhost:27017/omega
export SECRET_KEY=your-secret-key
export FEDERATION_CORE_URL=http://localhost:9400

# Run the service
python -m core.services.mcp_registry.service
```

## 📡 API Endpoints

### Health & Monitoring
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics
- `GET /info` - Service information
- `GET /ready` - Readiness probe
- `GET /live` - Liveness probe
- `POST /heartbeat` - Service heartbeat

### Tool Management
- `GET /tools` - List all active tools
- `POST /tools/register` - Register a new tool
- `POST /tools/{tool_id}/heartbeat` - Update tool heartbeat

### Server Management
- `GET /servers` - List all server configurations
- `POST /servers/register` - Register a new server
- `POST /servers/{name}/start` - Start a server
- `POST /servers/{name}/stop` - Stop a server
- `GET /servers/{name}/status` - Get server status

### Discovery
- `GET /discover` - Discover all MCP capabilities
- `POST /query-capabilities` - Query servers by capability
- `POST /recommend` - Get server recommendation for task

## 🔧 Configuration

The service uses the OMEGA Settings Service for configuration management with hot-reload support.

### Required Configuration
- `REDIS_URL` - Redis connection URL
- `MONGODB_URI` - MongoDB connection URI
- `SECRET_KEY` - Secret key for encryption
- `FEDERATION_CORE_URL` - Federation Core endpoint

### Optional Configuration
- `LOG_LEVEL` - Logging level (default: info)
- `MCP_REGISTRY_PORT` - Service port (default: 9402)
- `OMEGA_ENV` - Environment (development/staging/production)

## 📦 Server Types

The registry supports multiple MCP server types:

1. **STDIO** - Process-based communication (e.g., npx servers)
2. **HTTP** - RESTful communication
3. **SSE** - Server-Sent Events
4. **WebSocket** - Real-time bidirectional communication

## 🔄 Server Configuration Example

```json
{
  "name": "filesystem-server",
  "config": {
    "type": "stdio",
    "command": "npx",
    "args": ["@modelcontextprotocol/server-filesystem"],
    "env": {
      "NODE_ENV": "production"
    },
    "auto_start": true,
    "restart_on_failure": true,
    "max_retries": 3,
    "health_check_interval": 30
  }
}
```

## 🧬 Integration with OMEGA Ecosystem

### Federation Core
The MCP Registry automatically registers all tools and servers with the Federation Core, making them discoverable by Titans and Agents.

### Discovery Service
Capabilities are automatically inferred from server configurations and exposed through the discovery API.

### Health Monitoring
- Automatic health checks every 30 seconds (configurable)
- Automatic restart on failure (if configured)
- Exponential backoff for retry attempts
- Dead server detection and cleanup

## 🛡️ Security

- All connections use secure configuration patterns
- Environment variables are validated on startup
- Fail-fast principle - no fallbacks
- Encrypted storage for sensitive data

## 📊 Monitoring

The service exposes Prometheus-compatible metrics:
- `mcp_registry_uptime_seconds` - Service uptime
- `mcp_tools_registered_total` - Total registered tools
- `mcp_servers_configured_total` - Total configured servers
- `mcp_registry_requests_total` - Total API requests

## 🔥 Development

### Running Tests
```bash
pytest tests/ -v --cov=core.services.mcp_registry
```

### Code Quality
```bash
# Format code
black .

# Lint code
ruff check .
```

## 📜 Following the OMEGA Doctrine

This service strictly adheres to the OMEGA Doctrine v1.0:

- **Classification**: Service (Foundational Infrastructure)
- **Purpose**: To BE the guardian of MCP components
- **Nature**: Singleton, containerized, focused responsibility
- **Foundation**: Built on FastMCP for tool exposure

### Sacred Principles
- **Survive**: Resilient with health monitoring and auto-recovery
- **Adapt**: Hot-reload configuration, dynamic discovery
- **Procreate**: Supports Genesis Protocol for new tool creation

## 🔱 The Brotherhood Creed

> "Family is forever. Clean code is divine. This is the way."

---

**OMEGA MCP Registry v1.0** - Forged by the Brotherhood of Titans
