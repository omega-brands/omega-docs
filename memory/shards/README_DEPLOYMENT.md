# 🧠 OMEGA Sharded Memory API - Deployment Guide

The Memory API is a dedicated FastAPI service that provides tenant-isolated memory shard storage with vector search capabilities.

**Port:** `9227`  
**Base URL:** `http://localhost:9227/memory`

---

## 🚀 Quick Start (Docker - Recommended)

### 1. Start all services (Qdrant + MongoDB + Memory API)

```bash
cd D:\Repos\OMEGA\omega-core\memory\shards
docker-compose up -d
```

This brings up:
- **Qdrant** on port `6333` (vector database)
- **MongoDB** on port `27017` (document storage)
- **Memory API** on port `9227` (FastAPI service)

### 2. Verify services are running

```bash
# Check all containers
docker-compose ps

# Check Memory API health
curl http://localhost:9227/health

# Check Qdrant
curl http://localhost:6333/health

# Check MongoDB
docker exec omega-memory-mongo mongosh --eval "db.adminCommand('ping')"
```

### 3. View logs

```bash
# All services
docker-compose logs -f

# Just Memory API
docker-compose logs -f memory-api

# Just Qdrant
docker-compose logs -f qdrant
```

### 4. Stop services

```bash
docker-compose down

# To also remove volumes (WARNING: deletes all data)
docker-compose down -v
```

---

## 🛠️ Local Development (Without Docker)

If you want to run the Memory API locally without Docker:

### Prerequisites

1. **Qdrant** running on `localhost:6333`
   ```bash
   docker run -p 6333:6333 qdrant/qdrant:latest
   ```

2. **MongoDB** running on `localhost:27017`
   ```bash
   docker run -p 27017:27017 mongo:6
   ```

3. **Redis** (optional) on `localhost:6379`
   ```bash
   docker run -p 6379:6379 redis:latest
   ```

### Start the Memory API

```bash
cd D:\Repos\OMEGA\omega-core\memory\shards
python start_local.py
```

The API will be available at `http://localhost:9227`

---

## 📡 API Endpoints

### Store Shards
```bash
POST /memory/store_shards
Content-Type: application/json

{
  "shards": [
    {
      "tenant_id": "default",
      "compartment_id": "public:default",
      "content": "The sky is blue",
      "memory_stage": "claim",
      "memory_mode": "propositional"
    }
  ]
}
```

### Retrieve Shards (Semantic Search)
```bash
POST /memory/retrieve_shards
Content-Type: application/json

{
  "query": "What color is the sky?",
  "k": 10
}
```

### Compose Context
```bash
POST /memory/compose
Content-Type: application/json

{
  "query": "Tell me about the sky",
  "k": 24,
  "purpose": "answering user question"
}
```

---

## 🔌 Frontend Integration

The Next.js frontend at `D:\Repos\flow` uses a proxy route to forward all `/api/memory/*` requests to the Memory API.

**Proxy Route:** `src/app/api/memory/[...path]/route.ts`

This means the frontend can use relative paths:
```typescript
// Frontend code
const response = await fetch("/api/memory/store_shards", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ shards }),
});
```

And it automatically gets proxied to `http://localhost:9227/memory/store_shards`

---

## 🔧 Environment Variables

The Memory API uses these environment variables (set in `docker-compose.yml`):

| Variable | Default | Description |
|----------|---------|-------------|
| `QDRANT_URL` | `http://localhost:6333` | Qdrant connection URL |
| `QDRANT_DISTANCE` | `COSINE` | Distance metric for vectors |
| `MONGODB_URI` | `mongodb://localhost:27017/omega_memory` | MongoDB connection string |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection (optional) |
| `SERVICE_PORT` | `9227` | Port for the Memory API |
| `LOG_LEVEL` | `info` | Logging level |
| `FRONTEND_URL` | `http://localhost:3000` | Frontend URL for CORS |

---

## 🧪 Testing

### Test the API directly

```bash
# Health check
curl http://localhost:9227/health

# Store a shard
curl -X POST http://localhost:9227/memory/store_shards \
  -H "Content-Type: application/json" \
  -d '{
    "shards": [{
      "tenant_id": "test",
      "compartment_id": "public:test",
      "content": "Test memory shard",
      "memory_stage": "claim"
    }]
  }'

# Retrieve shards
curl -X POST http://localhost:9227/memory/retrieve_shards \
  -H "Content-Type: application/json" \
  -d '{
    "query": "test memory",
    "k": 5
  }'
```

### Test through the Next.js proxy

1. Start the Memory API (via Docker or locally)
2. Start the Next.js dev server:
   ```bash
   cd D:\Repos\flow
   npm run dev
   ```
3. Open `http://localhost:3000/memory`
4. Use the UI to ingest and search shards

---

## 🐛 Troubleshooting

### Memory API won't start

**Check if port 9227 is already in use:**
```bash
netstat -ano | findstr :9227
```

**Check Docker logs:**
```bash
docker-compose logs memory-api
```

### Qdrant connection errors

**Verify Qdrant is running:**
```bash
curl http://localhost:6333/health
```

**Check Qdrant logs:**
```bash
docker-compose logs qdrant
```

### MongoDB connection errors

**Verify MongoDB is running:**
```bash
docker exec omega-memory-mongo mongosh --eval "db.adminCommand('ping')"
```

**Check MongoDB logs:**
```bash
docker-compose logs mongodb
```

### CORS errors from frontend

Make sure `FRONTEND_URL` in `docker-compose.yml` matches your Next.js dev server URL (default: `http://localhost:3000`)

---

## 🔱 This is the way.

The Memory API is now part of the OMEGA Pantheon infrastructure. It provides the foundation for persistent, tenant-isolated memory across all Titans.

**Family is forever.**

