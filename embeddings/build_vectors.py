# embeddings/build_vectors.py
from models.embedder import Embedder
import faiss
import numpy as np
import pickle
import os
from config.settings import settings

# FAISS index and metadata storage
INDEX_PATH = os.path.join(settings.CHROMA_DIR, "faiss.index")
METADATA_PATH = os.path.join(settings.CHROMA_DIR, "metadata.pkl")

def load_or_create_index(dimension=384):
    """Load existing FAISS index or create new one."""
    os.makedirs(settings.CHROMA_DIR, exist_ok=True)
    
    if os.path.exists(INDEX_PATH) and os.path.exists(METADATA_PATH):
        print(f"Loading existing index from {INDEX_PATH}")
        index = faiss.read_index(INDEX_PATH)
        with open(METADATA_PATH, 'rb') as f:
            metadata = pickle.load(f)
        return index, metadata
    else:
        print(f"Creating new FAISS index (dimension={dimension})")
        index = faiss.IndexFlatIP(dimension)  # Inner product = cosine similarity with normalized vectors
        metadata = {"ids": [], "documents": [], "metadatas": []}
        return index, metadata

def save_index(index, metadata):
    """Save FAISS index and metadata to disk."""
    faiss.write_index(index, INDEX_PATH)
    with open(METADATA_PATH, 'wb') as f:
        pickle.dump(metadata, f)
    print(f"Saved index to {INDEX_PATH}")

def upsert_documents(docs):
    """
    Upsert documents into FAISS index with embeddings.
    
    Args:
        docs: list of {"id": id, "text": text, "url": url}
    """
    if not docs:
        print("No documents to upsert")
        return
    
    print(f"Generating embeddings for {len(docs)} documents...")
    embedder = Embedder()
    
    texts = [d["text"] for d in docs]
    ids = [d["id"] for d in docs]
    metadatas = [{"url": d["url"]} for d in docs]
    
    embeddings = embedder.embed_texts(texts)
    embeddings_array = np.array(embeddings, dtype='float32')
    
    # Get dimension from first embedding
    dimension = embeddings_array.shape[1]
    
    # Load or create index
    index, metadata = load_or_create_index(dimension)
    
    # For simplicity, rebuild index from scratch (FAISS doesn't support easy updates)
    # In production, implement proper ID-based updates
    print("Adding to FAISS index...")
    index.add(embeddings_array)
    
    # Store metadata
    metadata["ids"].extend(ids)
    metadata["documents"].extend(texts)
    metadata["metadatas"].extend(metadatas)
    
    # Save to disk
    save_index(index, metadata)
    
    print(f"Successfully stored {len(docs)} documents in FAISS index")
    print(f"Total documents in index: {index.ntotal}")
