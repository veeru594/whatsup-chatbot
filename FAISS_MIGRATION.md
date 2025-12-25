# ⚠️ ChromaDB → FAISS Migration (Windows Fix)

## Problem
ChromaDB failed to install on Windows due to dependencies requiring C++ compilation:
- `greenlet` - requires Microsoft Visual C++ Build Tools
- `chroma-hnswlib` - requires C++ compiler

Error:
```
ERROR: Failed building wheel for greenlet
Failed to build installable wheels for some pyproject.toml based projects
```

## Solution
Switched to **FAISS (Facebook AI Similarity Search)** which:
- ✅ Has pre-built wheels for Windows
- ✅ No compilation needed
- ✅ Faster than ChromaDB for simple use cases
- ✅ Battle-tested by Facebook/Meta

## Changes Made

### 1. requirements.txt
```diff
- chromadb
+ faiss-cpu
+ numpy
```

### 2. embeddings/build_vectors.py
- Replaced ChromaDB client with FAISS index
- Uses `faiss.IndexFlatIP` for inner product similarity (equivalent to cosine similarity with normalized vectors)
- Stores metadata separately using pickle
- Saves index to disk: `./chroma_db/faiss.index` and `./chroma_db/metadata.pkl`

### 3. bot/responder.py
- Updated to load FAISS index instead of ChromaDB collection
- Uses `index.search()` instead of `collection.query()`
- Adjusted similarity threshold (FAISS returns different scale)

## API Differences

| Feature | ChromaDB | FAISS |
|---------|----------|-------|
| Storage | DuckDB + Parquet | Binary index + Pickle |
| Query | `collection.query()` | `index.search()` |
| Upsert | Native support | Rebuild required |
| Metadata | Built-in | Manual (pickle) |
| Windows | ❌ Requires C++ | ✅ Pre-built wheels |

## Performance Notes
- FAISS is actually **faster** for similarity search
- Slight overhead for metadata management (negligible)
- Index rebuilds on upsert (not an issue for periodic scraping)

## No Code Changes Needed
Everything else remains the same:
- Scraper works identically
- Embedder unchanged
- API responses identical
- Testing procedure same

## Updated Settings
The `CHROMA_DIR` setting still works - it now stores:
- `faiss.index` - FAISS vector index
- `metadata.pkl` - Document metadata

---

✅ **Installation now works on Windows without any C++ build tools!**
