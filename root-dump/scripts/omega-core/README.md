# 🚀⚛️ LEGENDARY OMEGA DEPLOYMENT SCRIPTS ⚛️🚀

**"Our superpositions have yet to be determined; therefore, anything you observe isn't us!"**

## 🎯 Quick Commands

### Standard Legendary Deployment
```bash
# From project root
./scripts/deploy.sh
```

### Nuclear Rebuild (When Things Get Weird)
```bash
# Nukes everything and rebuilds from scratch
./scripts/nuclear_rebuild.sh
```

### Full Manual Control
```bash
# Run the full legendary deployment script
./scripts/legendary_deployment.sh
```

## 📋 What Each Script Does

### `legendary_deployment.sh` 🚀
The main deployment beast that:
- Builds all services with `--no-cache`
- Uses existing docker-compose.yml configuration
- Deploys entire Omega ecosystem
- Runs health checks
- Shows all service endpoints
- Provides management commands

### `deploy.sh` ⚡
Quick launcher that just runs the legendary deployment script with proper permissions.

### `nuclear_rebuild.sh` 💥
The "nuke it from orbit" option that:
- Stops all containers
- Removes all Omega images
- Clears all Docker cache
- Runs legendary deployment fresh

## 🎯 Service Ports (from docker-ports.csv)

| Service | Port | Endpoint |
|---------|------|----------|
| MCP Registry | 9402 | http://localhost:9402 |
| Calculator | 9202 | http://localhost:9202 |
| Code Analyzer | 9208 | http://localhost:9208 |
| SQL Executor | 9201 | http://localhost:9201 |
| NLP to SQL | 9203 | http://localhost:9203 |
| Text Summarizer | 9204 | http://localhost:9204 |
| Text Translator | 9205 | http://localhost:9205 |
| Web Search | 9206 | http://localhost:9206 |
| Dependency Resolver | 9209 | http://localhost:9209 |
| MongoDB | 27017 | mongodb://localhost:27017 |
| Redis | 6379 | redis://localhost:6379 |

## 🛠️ Management Commands

```bash
# View logs
docker-compose logs -f

# Stop everything
docker-compose down

# Restart a specific service
docker-compose restart calculator

# Scale a service
docker-compose up -d --scale calculator=3

# Check status
docker-compose ps
```

## 🚨 Troubleshooting

### If a service won't start:
```bash
# Check logs for that service
docker-compose logs calculator

# Restart just that service
docker-compose restart calculator
```

### If builds are failing:
```bash
# Use nuclear option
./scripts/nuclear_rebuild.sh
```

### If ports are conflicting:
```bash
# Check what's using the port
lsof -i :9202

# Kill the process if needed
kill -9 <PID>
```

## 🎉 Success Indicators

When everything is legendary, you'll see:
- ✅ All services showing "LEGENDARY" in health check
- 🟢 All containers in "Up" status
- 🚀 All endpoints responding to HTTP requests
- ⚛️ No error messages in logs

## 🔗 Redis Auth & URLs

The `env_watcher.py` script supports various Redis connection formats:

### URL Format Examples
```bash
# Password only (most common for Redis containers)
redis://:PASSWORD@host:6379/0

# Username and password
redis://USER:PASSWORD@host:6379/0

# TLS connection (rediss://)
rediss://USER:PASSWORD@host:6380/0

# Local development
redis://localhost:6379/0
```

### Setting REDIS_URL in PowerShell
```powershell
# Set for current session
$env:REDIS_URL = "redis://:E73wdsGrH6^Y37QRkC7@redis:6379/0"

# Set permanently for user
[Environment]::SetEnvironmentVariable("REDIS_URL", "redis://:E73wdsGrH6^Y37QRkC7@redis:6379/0", "User")
```

**LFG!!! 🚀🚀🚀**
