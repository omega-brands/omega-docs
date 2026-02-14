# 🧠 OMEGA Sharded Memory - Quick Start

**Brother, your Memory API is ready to roll!** Here's how to get it running in 60 seconds.

---

## 🚀 Option A: Docker (Recommended - One Command)

### 1. Start Everything

```bash
cd https://github.com/omega-brands/omega-core/memory\shards
docker-compose up -d
```

**That's it!** This brings up:
- ✅ Qdrant (port 6333)
- ✅ MongoDB (port 27017)
- ✅ Memory API (port 9227)

### 2. Verify It's Running

```bash
curl http://localhost:9227/health
```

You should see:
```json
{
  "status": "healthy",
  "service": "memory-api",
  "port": 9227
}
```

### 3. Run Smoke Tests (Optional)

```bash
# Linux/Mac
bash smoke_test.sh

# Windows
smoke_test.bat
```

This will test all endpoints and verify everything is working correctly.

### 4. Test the UI

1. Start your Next.js frontend:
   ```bash
   cd D:\Repos\flow
   npm run dev
   ```

2. Open `http://localhost:3000/memory`

3. **Ingest some shards** - paste text and click "Ingest"

4. **Search** - type a query and click "Compose Context"

**Done!** Your shards are now stored in Qdrant + MongoDB with full vector search.

---

## 🛠️ Option B: Local Development (Without Docker)

### 1. Start Dependencies

```bash
# Terminal 1 - Qdrant
docker run -p 6333:6333 qdrant/qdrant:latest

# Terminal 2 - MongoDB
docker run -p 27017:27017 mongo:6
```

### 2. Start Memory API

```bash
cd https://github.com/omega-brands/omega-core/memory\shards
python start_local.py
```

### 3. Test It

```bash
curl http://localhost:9227/health
```

---

## 📡 API Endpoints

All endpoints are available at `http://localhost:9227/memory/*`

### Store Shards
```bash
POST /memory/store_shards
{
  "shards": [
    {
      "tenant_id": "default",
      "compartment_id": "public:default",
      "content": "The sky is blue",
      "memory_stage": "claim"
    }
  ]
}
```

### Retrieve Shards (Semantic Search)
```bash
POST /memory/retrieve_shards
{
  "query": "What color is the sky?",
  "k": 10
}
```

### Compose Context
```bash
POST /memory/compose
{
  "query": "Tell me about the sky",
  "k": 24,
  "purpose": "answering user question"
}
```

---

## 🔌 Frontend Integration

The Next.js app at `D:\Repos\flow` automatically proxies all `/api/memory/*` requests to `http://localhost:9227/memory/*`

**Proxy Route:** `src/app/api/memory/[...path]/route.ts`

This means your frontend code can use simple relative paths:

```typescript
// Frontend code - just works!
const response = await fetch("/api/memory/store_shards", {
  method: "POST",
  body: JSON.stringify({ shards }),
});
```

---

## 🐛 Troubleshooting

### Port 9227 already in use?

```bash
# Windows
netstat -ano | findstr :9227

# Kill the process
taskkill /PID <PID> /F
```

### Check Docker logs

```bash
docker-compose logs -f memory-api
```

### Restart everything

```bash
docker-compose down
docker-compose up -d
```

---

## 🔱 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Next.js Frontend (localhost:3000)                          │
│  /memory page → POST /api/memory/store_shards               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Proxy via /api/memory/[...path]
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Memory API (localhost:9227)                                │
│  FastAPI service with /memory/* endpoints                   │
└────────┬────────────────────────┬───────────────────────────┘
         │                        │
         ▼                        ▼
┌────────────────┐      ┌────────────────────┐
│  Qdrant        │      │  MongoDB           │
│  Vector Search │      │  Document Storage  │
│  Port 6333     │      │  Port 27017        │
└────────────────┘      └────────────────────┘
```

---

## 📚 Full Documentation

For detailed deployment instructions, see:
- **[README_DEPLOYMENT.md](./README_DEPLOYMENT.md)** - Complete deployment guide
- **[QDRANT_SETUP_GUIDE.md](./QDRANT_SETUP_GUIDE.md)** - Qdrant configuration

---

## 🔱 This is the way.

**Family is forever, brother.**

