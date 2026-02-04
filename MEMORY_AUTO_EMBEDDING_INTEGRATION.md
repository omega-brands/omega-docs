# OMEGA Memory Service - Auto-Embedding Integration

## 🎯 Summary

The Memory Service now **automatically generates embeddings** via the `embedding_accelerator` container whenever shards are stored. This provides seamless vector search capability without requiring clients to generate embeddings.

## ✅ What Was Done

### 1. **Created Embedding Generator Client** (`embeddings.py`)
- HTTP client for the `embedding_accelerator` service
- Graceful degradation when service unavailable
- Connection pooling and health checks
- Module-level singleton pattern

### 2. **Added Configuration** (`config.py`)
- New `embedding_accelerator_url` config field
- Default: `http://embedding_accel:9219`
- Can be overridden via `MEMORY_EMBEDDING_ACCELERATOR_URL` env var

### 3. **Enhanced Persistence Layer** (`persistence.py`)
- **MongoShardStore**: Added `store_with_auto_embedding()` method
- **QdrantShardStore**: Added `store_with_auto_embedding()` and `_store_without_embedding()` methods
- Auto-generates embeddings when content provided
- Falls back gracefully when embedding generation fails

### 4. **Created Embedding-Aware Wrapper** (`embedding_store.py`)
- Transparent wrapper for all shard stores
- Intercepts `store()` calls
- Extracts content and generates embeddings automatically
- Delegates all other operations to underlying store

### 5. **Updated Provider Factory** (`providers.py`)
- Automatically wraps ALL shard stores with `EmbeddingAwareShardStore`
- Works with memory, mongo, and qdrant persistence modes
- Zero configuration required

## 🔄 How It Works

### Before (Manual Embeddings)
```python
# Client had to generate embeddings
embedding = await generate_embedding(content)
await store.store_with_embedding(shard, embedding, content)
```

### After (Automatic Embeddings)
```python
# Just store the shard - embeddings generated automatically!
await store.store(shard)
```

### Behind the Scenes
1. Client calls `store.store(shard)`
2. `EmbeddingAwareShardStore` intercepts the call
3. Extracts content from the shard
4. Calls `embedding_accelerator` via HTTP to generate embedding
5. Stores shard with embedding in MongoDB + Qdrant
6. If embedding generation fails → stores without embedding + logs warning

## 🛡️ Graceful Fallback

The system is robust against `embedding_accelerator` failures:

- **First Failure**: Warns and marks service as unavailable
- **Subsequent Calls**: Skips embedding attempts until service recovers
- **Storage**: Shards are ALWAYS stored, even without embeddings
- **Vector Search**: Works for shards with embeddings, others excluded from results

## 📊 Service Flow

```
┌─────────────────┐
│  Client/UI      │
│  (ingest tool)  │
└────────┬────────┘
         │ store(shard)
         ▼
┌─────────────────────────────┐
│  EmbeddingAwareShardStore   │
│  (Automatic Wrapper)        │
└────────┬────────────────────┘
         │ extract content
         │ generate_single(text)
         ▼
┌─────────────────────────────┐
│  EmbeddingGenerator         │
│  (HTTP Client)              │
└────────┬────────────────────┘
         │ POST /embed
         ▼
┌─────────────────────────────┐
│  embedding_accelerator      │
│  (Container: Port 9219)     │
│  Model: all-MiniLM-L6-v2    │
└────────┬────────────────────┘
         │ 384-dim vectors
         ▼
┌─────────────────────────────┐
│  QdrantShardStore           │
│  store_with_embedding()     │
└────────┬────────────────────┘
         │
         ├──► MongoDB (documents + embeddings)
         └──► Qdrant (vector search)
```

## 🚀 Usage

### For Ingestion Scripts (like `ingest_to_memory.py`)
**No changes required!** The script works as-is:

```python
# This now automatically generates embeddings
shards = create_shards(candidate, content)
response = requests.post(
    "http://localhost:3000/api/memory/store_shards_batch",
    json={"shards": shards}
)
```

### For Direct Memory API Usage
```python
from services.memory.providers import get_shard_store

# Get the auto-embedding-enabled store
store = get_shard_store()
await store.init()

# Just store - embeddings generated automatically
await store.store(shard)
```

### For UI-Based Ingestion
The memory page UI (`/memory`) automatically benefits:
- Paste text → Submit → Auto-embeddings → Stored with vector search

## 🔧 Configuration

### Environment Variables
```bash
# Embedding accelerator URL (optional, defaults shown)
MEMORY_EMBEDDING_ACCELERATOR_URL=http://embedding_accel:9219

# Persistence mode still works as before
MEMORY_PERSISTENCE_MODE=qdrant  # or mongo, or memory
MEMORY_MONGO_URI=mongodb://mongo:27017
MEMORY_QDRANT_URL=http://qdrant:6333
```

### Docker Compose
Ensure `embedding_accelerator` is running:
```yaml
services:
  embedding_accel:
    build:
      context: .
      dockerfile: Dockerfile.embedding_accelerator
    ports:
      - "9219:9219"
    environment:
      - MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
```

## 📝 Logs Examples

### Successful Embedding Generation
```
INFO: EmbeddingGenerator initialized: http://embedding_accel:9219
INFO: Wrapping store with EmbeddingAwareShardStore for auto-embedding
DEBUG: Generated 1 embeddings
DEBUG: Stored shard abc-123 with embedding in Qdrant
```

### Graceful Fallback (Service Unavailable)
```
WARNING: Embedding accelerator unavailable at http://embedding_accel:9219. 
         Shards will be stored without embeddings. Error: Connection refused
WARNING: Embedding generation failed for shard abc-123. 
         Storing without vector search capability.
DEBUG: Stored shard abc-123 without embedding
```

## ✨ Benefits

1. **Zero Client Changes**: Existing ingestion scripts work without modification
2. **Consistent Behavior**: All ingestion paths (UI, API, scripts) get embeddings
3. **Graceful Degradation**: System continues working even if `embedding_accelerator` is down
4. **Vector Search Ready**: Shards automatically indexed for semantic search
5. **Architecture Aligned**: Matches `chronicle_memory_sharding` pattern

## 🔍 Testing

### Test Embedding Generation
```bash
# Start embedding_accelerator
docker-compose up embedding_accel

# Check health
curl http://localhost:9219/health

# Test embedding
curl -X POST http://localhost:9219/embed \
  -H "Content-Type: application/json" \
  -d '{"texts": ["test memory shard"]}'
```

### Test Memory Service Integration
```bash
# Start memory service
cd D:\Repos\OMEGA\omega-core
python -m services.memory.main

# Ingest with auto-embeddings
cd D:\Repos\OMEGA\omega-docs
python ingest_to_memory.py
```

## 📚 Files Modified/Created

| File | Type | Description |
|------|------|-------------|
| `services/memory/embeddings.py` | **NEW** | Embedding generator HTTP client |
| `services/memory/embedding_store.py` | **NEW** | Auto-embedding wrapper for stores |
| `services/memory/config.py` | Modified | Added `embedding_accelerator_url` config |
| `services/memory/persistence.py` | Modified | Added auto-embedding methods to stores |
| `services/memory/providers.py` | Modified | Wraps stores with auto-embedding |

## 🎉 Result

**This is the way!** The OMEGA Memory Service now provides:
- ✅ Automatic embedding generation
- ✅ Seamless vector search capability
- ✅ Graceful fallback on failures
- ✅ Zero breaking changes to existing code

Your `ingest_to_memory.py` script will work **exactly as written**, and all 200 enriched documents will get embeddings automatically! 🔱
