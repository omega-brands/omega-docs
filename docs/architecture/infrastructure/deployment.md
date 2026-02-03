# Deployment Guide: OMEGA Core Bring-Up

Complete deployment checklist for bringing up OMEGA Core services in production and development environments.

## 🎯 Overview

This guide covers the full deployment process for OMEGA Core, from prerequisites through verification and production readiness.

### Deployment Targets

- 🐳 **Docker Desktop (Windows)** - Local development
- 🐧 **Docker Compose (Linux)** - Server deployment
- ☸️ **Kubernetes** - Production orchestration
- ☁️ **Cloud Platforms** - AWS, GCP, Azure

---

## 📋 Prerequisites

### System Requirements

**Minimum:**
- CPU: 4 cores
- RAM: 8 GB
- Disk: 50 GB SSD
- OS: Windows 10+, Ubuntu 20.04+, or macOS 12+

**Recommended:**
- CPU: 8+ cores
- RAM: 16+ GB
- Disk: 100+ GB NVMe SSD
- OS: Ubuntu 22.04 LTS

### Software Requirements

- ✅ **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
- ✅ **Docker Compose** v2.0+
- ✅ **PowerShell** 7+ (Windows) or **Bash** (Linux/Mac)
- ✅ **Git** 2.30+
- ✅ **curl** or **httpie** for testing

### Repository Setup

```bash
# Clone repository
git clone https://github.com/omega-framework/omega.git
cd omega

# Verify structure
ls -la
# Should see: core/, services/, agents/, tools/, .env.example
```

---

## ⚙️ Environment Configuration

### Step 1: Create Environment File

```bash
# Copy template
cp .env.example .env

# Edit configuration
nano .env  # or your preferred editor
```

### Step 2: Core Service URLs

> Note: Prefer the base URL + gateway pattern for identities and derived endpoints. See: /docs/operations/gateway-ingress


```dotenv
# Core service URLs (Docker network DNS)
FEDERATION_CORE_URL=http://federation_core:9405
AGENT_REGISTRY_URL=http://agent_registry:9401
MCP_REGISTRY_URL=http://mcp_registry:9402
CONTEXT_SERVER_URL=http://context_server:9411

# Legacy/Entity defaults (compatibility)
FEDERATION_URL=http://federation_core:9405
REGISTRY_URL=http://agent_registry:9401

# Heartbeat configuration
HEARTBEAT_INTERVAL=30
```

### Step 3: Database Configuration

```dotenv
# MongoDB
MONGODB_URI=mongodb://mongo:27017/omega
MONGODB_DATABASE=omega

# Redis
REDIS_URL=redis://:your-password@redis:6379/0
REDIS_PASSWORD=your-secure-password

# PostgreSQL (if using)
POSTGRES_URI=postgresql://user:pass@postgres:5432/omega
```

### Step 4: Security Configuration

```dotenv
# Secret keys (generate unique values!)
SECRET_KEY=your-secret-key-min-32-chars
CONFIG_MSG_HMAC_KEY=your-hmac-key-min-32-chars

# Encryption
OMEGA_FERNET_KEY=your-fernet-key-base64-encoded

# Certificate Authority
CA_PASSPHRASE=your-ca-passphrase
CERT_EXPIRY_DAYS=365
```

**Generate secure keys:**

```bash
# Generate SECRET_KEY
openssl rand -hex 32

# Generate Fernet key
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Generate HMAC key
openssl rand -base64 32
```

---

## 🚀 Deployment Steps

### Docker Compose Deployment

#### Step 1: Pull Images

```powershell
# Navigate to core directory
cd D:\repos\omega\core

# Pull latest images
docker compose pull
```

#### Step 2: Build Services

```powershell
# Build all services
docker compose up -d --build
```

**Build Output:**
```
[+] Building 45.2s (23/23) FINISHED
[+] Running 8/8
 ✔ Container omega-redis-1              Started
 ✔ Container omega-mongo-1              Started
 ✔ Container omega-federation-core-1    Started
 ✔ Container omega-agent-registry-1     Started
 ✔ Container omega-mcp-registry-1       Started
 ✔ Container omega-context-server-1     Started
 ✔ Container omega-orchestrator-1       Started
```

#### Step 3: Verify Containers

```powershell
# Check container status
docker ps --format "table {{.Names}}\t{{.Ports}}\t{{.Status}}"
```

**Expected Output:**
```
NAMES                        PORTS                    STATUS
omega-federation-core-1      0.0.0.0:9405->9405/tcp   Up 30 seconds
omega-agent-registry-1       0.0.0.0:9401->9401/tcp   Up 30 seconds
omega-mcp-registry-1         0.0.0.0:9402->9402/tcp   Up 30 seconds
omega-orchestrator-1         0.0.0.0:9000->9000/tcp   Up 30 seconds
omega-redis-1                0.0.0.0:6379->6379/tcp   Up 32 seconds
omega-mongo-1                0.0.0.0:27017->27017/tcp Up 32 seconds
```


### Gateway-first Verification (Recommended)

Use the local gateway (nginx) that mirrors Azure AGW. Services publish portless identities via gateway, and agents derive register/heartbeat from AGENT_REGISTRY_BASE.

```bash
# Health via gateway
curl -sf http://localhost:8080/api/core/agent_registry/health
curl -sf http://localhost:8080/api/titans/claude/health

# Optional flip: route internal calls via gateway
# export AGENT_REGISTRY_BASE=http://gateway/api/core/agent_registry
```

---

## ✅ Post-Deployment Verification

> Note: Prefer gateway-first health checks for local + cloud parity. Direct port endpoints below are legacy/debug convenience.
> See: /docs/operations/gateway-ingress


### Health Check Commands

#### Federation Core

```bash
# Check Federation Core health
curl -s http://localhost:9405/health | jq

# Expected Output:
{
  "status": "healthy",
  "id": "federation_core",
  "type": "service",
  "timestamp": "2025-01-20T10:30:00Z",
  "uptime": 30
}
```

#### FastMCP Directory Resource

```bash
# Check directory resource
curl -s http://localhost:9405/mcp/resources/omega/directory/servers | jq

# Expected Output:
{
  "servers": [
    {
      "id": "code_analyzer_fastmcp",
      "name": "Code Analyzer",
      "status": "active",
      "endpoints": {
        "mcp": "http://code-analyzer:9501/mcp"
      }
    }
  ]
}
```

#### Agent Registry

```bash
# Check Agent Registry health
curl -s http://localhost:9401/agent_registry/health | jq

# Expected Output:
{
  "status": "healthy",
  "service_id": "agent_registry",
  "registered_agents": 3,
  "timestamp": "2025-01-20T10:30:00Z"
}
```

#### Orchestrator Agent

```bash
# Main app health
curl -s http://localhost:9000/health | jq

# MCP app health
curl -s http://localhost:9001/mcp/health | jq
```

#### Tool Servers

```bash
# Example tool server health
curl -s http://localhost:9420/health | jq

# Expected Output:
{
  "status": "healthy",
  "name": "calculator_tool",
  "type": "tool",
  "version": "1.0.0"
}
```

---

## 🔍 Acceptance Criteria

### ✅ Deployment Success Checklist

- [ ] All `docker compose` commands execute without errors
- [ ] `docker ps` shows all containers in "Up" status
- [ ] All health endpoints return `200 OK` with `"status": "healthy"`
- [ ] Federation Core `/mcp/resources` returns registered services
- [ ] Agent Registry reports registered agents
- [ ] No error logs in `docker compose logs`
- [ ] Redis connection successful
- [ ] MongoDB connection successful

### Automated Verification Script

```bash
#!/bin/bash
# verify_deployment.sh

echo "🔍 Verifying OMEGA Core Deployment..."

# Array of services to check
services=(
  "http://localhost:9405/health:Federation Core"
  "http://localhost:9401/agent_registry/health:Agent Registry"
  "http://localhost:9402/mcp/health:MCP Registry"
  "http://localhost:9000/health:Orchestrator"
)

failed=0

for service in "${services[@]}"; do
  url="${service%%:*}"
  name="${service##*:}"

  echo -n "Checking $name... "

  status=$(curl -s -o /dev/null -w "%{http_code}" "$url")

  if [ "$status" = "200" ]; then
    echo "✅ OK"
  else
    echo "❌ FAILED (HTTP $status)"
    failed=$((failed + 1))
  fi
done

if [ $failed -eq 0 ]; then
  echo "✅ All services healthy!"
  exit 0
else
  echo "❌ $failed service(s) failed"
  exit 1
fi
```

---

## 🐛 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker compose logs federation_core --tail=100

# Check resource usage
docker stats

# Restart specific service
docker compose restart federation_core
```

### Network Connectivity Issues

```bash
# Test inter-container communication
docker compose exec federation_core curl http://agent_registry:9401/health

# Check Docker network
docker network ls
docker network inspect omega_default
```

### Port Conflicts

```bash
# Check port usage (Windows)
netstat -ano | findstr :9405

# Check port usage (Linux/Mac)
lsof -i :9405

# Kill process using port
# Windows: taskkill /PID <pid> /F
# Linux/Mac: kill -9 <pid>
```

### Database Connection Failures

```bash
# Test MongoDB connection
docker compose exec mongo mongosh --eval "db.runCommand({ping: 1})"

# Test Redis connection
docker compose exec redis redis-cli ping
```

---

## 🔄 Updates and Maintenance

### Rolling Update

```bash
# Pull latest images
docker compose pull

# Recreate services with zero downtime
docker compose up -d --no-deps --build federation_core
docker compose up -d --no-deps --build agent_registry
# ... repeat for each service
```

### Backup and Restore

```bash
# Backup MongoDB
docker compose exec mongo mongodump --out /backup

# Backup Redis
docker compose exec redis redis-cli SAVE

# Copy backups to host
docker cp omega-mongo-1:/backup ./mongo_backup
docker cp omega-redis-1:/data/dump.rdb ./redis_backup
```

### Log Management

```bash
# View logs
docker compose logs -f --tail=100

# Export logs
docker compose logs > omega_logs_$(date +%Y%m%d).log

# Rotate logs
docker compose logs --since 24h > recent_logs.log
```

---

## ☸️ Kubernetes Deployment

### Helm Chart Installation

```bash
# Add OMEGA Helm repository
helm repo add omega https://charts.omega.dev
helm repo update

# Install OMEGA Core
helm install omega-core omega/omega \
  --namespace omega \
  --create-namespace \
  --values values.yaml
```

### values.yaml

```yaml
replicaCount: 3

federation:
  enabled: true
  replicas: 3
  resources:
    requests:
      memory: "512Mi"
      cpu: "500m"
    limits:
      memory: "1Gi"
      cpu: "1000m"

redis:
  enabled: true
  auth:
    password: "your-redis-password"

mongodb:
  enabled: true
  auth:
    rootPassword: "your-mongo-password"
```

---

## 📚 Next Steps

- [Security Best Practices](/docs/security/best-practices) - Hardening your deployment
- [Monitoring & Observability](/docs/intro) - Production monitoring
- [Scaling Guide](/docs/intro) - Horizontal and vertical scaling

**🏛️ Deploy with confidence. The Brotherhood protects the infrastructure.**
