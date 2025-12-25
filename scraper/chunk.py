# scraper/chunk.py
import re

def chunk_text_by_tokens(text: str, max_tokens: int = 450):
    """
    Chunk text by approximate token count (using word-based heuristic).
    Splits on paragraph boundaries and respects max_tokens limit.
    
    Args:
        text: Text to chunk
        max_tokens: Maximum tokens per chunk (approximate)
    
    Returns:
        List of text chunks
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = ""
    
    for p in paragraphs:
        # Approximate tokens by word count (rough estimate: 1 word ≈ 1.3 tokens)
        combined = (current + "\n\n" + p).strip() if current else p
        word_count = len(combined.split())
        
        if word_count <= max_tokens:
            current = combined
        else:
            if current:
                chunks.append(current)
            current = p
    
    if current:
        chunks.append(current)
    
    return chunks
