# 🧠 Memory API Setup Guide

## Problem Fixed

The error `{"error":"fetch failed"}` was occurring because the Memory API service wasn't running on port 9227.

## Solution Implemented

I've created **mock API endpoints** that allow the frontend to work without the backend service running. This is perfect for frontend development!

### Files Created

1. **`src/app/api/memory/store_shards_batch/route.ts`** - Mock endpoint for storing memory shards
2. **`src/app/api/memory/compose/route.ts`** - Mock endpoint for composing memory context
3. **Updated `src/app/memory/page.tsx`** - Added mock mode detection and warning banners

### Mock Mode Features

- ✅ **Automatic Detection** - The UI automatically detects when using mock data
- ✅ **Visual Warnings** - Yellow warning banner shows when in mock mode
- ✅ **Realistic Responses** - Mock endpoints return realistic data structures
- ✅ **Console Logging** - Mock operations are logged to the console
- ✅ **No Backend Required** - Frontend works independently for development

## How to Use

### Option 1: Continue with Mock Mode (Current Setup)

Just use the app as-is! The mock endpoints will handle all requests.

**Pros:**
- No backend setup required
- Perfect for UI/UX development
- Fast iteration

**Cons:**
- Data is not persisted
- No real vector search
- No real embeddings

### Option 2: Start the Real Memory API Service

If you want real functionality with vector search and persistent storage:

#### Prerequisites

1. **Qdrant** (Vector Database) - Port 6333
2. **MongoDB** (Document Storage) - Port 27017
3. **Memory API** (FastAPI Service) - Port 9227

#### Quick Start with Docker

```powershell
# Navigate to OMEGA repository
cd D:\Repos\OMEGA\omega-core

# Start all memory services
docker-compose up -d memory-api qdrant mongodb
```

#### Or Start Locally (Without Docker)

```powershell
# Navigate to memory shards directory
cd https://github.com/omega-brands/omega-core/memory\shards

# Start the service
python start_local.py
```

**Note:** Local mode requires Qdrant and MongoDB to be running separately.

#### Verify Service is Running

```powershell
# Check health endpoint
curl http://localhost:9227/health

# Should return:
# {"status":"healthy","service":"memory-api","port":9227}
```

### Option 3: Remove Mock Endpoints (When Backend is Ready)

Once the Memory API service is running, you can remove the mock endpoints:

```powershell
# Delete mock endpoints
Remove-Item src/app/api/memory/store_shards_batch/route.ts
Remove-Item src/app/api/memory/compose/route.ts
```

The catch-all proxy at `src/app/api/memory/[...path]/route.ts` will then handle all requests.

## Architecture

```
┌─────────────────┐
│   Next.js App   │
│  (Port 3000)    │
└────────┬────────┘
         │
         │ POST /api/memory/store_shards_batch
         │ POST /api/memory/compose
         ▼
┌─────────────────────────────────────┐
│  Mock Endpoints (Current)           │
│  OR                                 │
│  Proxy → Memory API (Port 9227)     │
└────────┬────────────────────────────┘
         │
         │ (When using real backend)
         ▼
┌─────────────────┐     ┌─────────────┐
│  Qdrant (6333)  │◄────┤ Memory API  │
│  Vector Search  │     │  (9227)     │
└─────────────────┘     └──────┬──────┘
                               │
                               ▼
                        ┌─────────────┐
                        │ MongoDB     │
                        │ (27017)     │
                        └─────────────┘
```

## Testing

### Test Mock Mode

1. Navigate to `http://localhost:3000/memory`
2. You should see a yellow warning banner: "Mock Mode Active"
3. Try ingesting some text - it will show "Mock Stored"
4. Try composing a query - it will return mock results

### Test Real Backend

1. Start the Memory API service (see Option 2 above)
2. Remove the mock endpoints (see Option 3 above)
3. Restart your Next.js dev server
4. Navigate to `http://localhost:3000/memory`
5. No warning banner should appear
6. Data will be persisted to MongoDB and searchable via Qdrant

## Troubleshooting

### "fetch failed" error returns

**Cause:** Memory API service is not running and mock endpoints were removed

**Solution:** Either:
- Restore mock endpoints, OR
- Start the Memory API service

### Mock mode doesn't show warning

**Cause:** The `_mock` flag is not being set in the response

**Solution:** Check that the mock endpoints are being used (not the proxy)

### Data not persisting

**Cause:** Using mock mode

**Solution:** Start the real Memory API service

## Next Steps

1. **For Frontend Development:** Continue using mock mode
2. **For Full Stack Testing:** Set up the Memory API service
3. **For Production:** Deploy all services via Docker Compose

---

**🔱 This is the way. Family is forever.**

