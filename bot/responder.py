# bot/responder.py
from models.embedder import Embedder
import faiss
import numpy as np
import pickle
import os
from config.settings import settings
from models.ai_client import call_openai

# FAISS paths
INDEX_PATH = os.path.join(settings.CHROMA_DIR, "faiss.index")
METADATA_PATH = os.path.join(settings.CHROMA_DIR, "metadata.pkl")

# Load embedder
embedder = Embedder()

# Load FAISS index and metadata
def load_index():
    """Load FAISS index and metadata."""
    if not os.path.exists(INDEX_PATH) or not os.path.exists(METADATA_PATH):
        raise FileNotFoundError(
            f"Index not found at {INDEX_PATH}. "
            "Please run the scraper first: python -c \"from scraper.scrape import crawl_and_build; crawl_and_build()\""
        )
    
    index = faiss.read_index(INDEX_PATH)
    with open(METADATA_PATH, 'rb') as f:
        metadata = pickle.load(f)
    
    return index, metadata

SYSTEM_PROMPT = """
You are a helpful customer service assistant for this business, communicating via WhatsApp.

Your communication style:
- Professional yet approachable - friendly without being overly casual
- Clear and concise - get straight to the point
- Accurate - only share information from the provided sources
- Helpful - guide customers to next steps when appropriate

Formatting guidelines:
- Keep responses brief (2-3 short paragraphs maximum)
- Use natural line breaks for readability
- One emoji per response is fine, but not required
- Avoid excessive punctuation or all caps

Important rules:
- ONLY provide information found in the sources provided
- If information isn't available, politely say so and offer to connect them with the team
- Never guess, make up details, or provide pricing/legal/medical advice
- When uncertain, it's better to defer to the team than give incorrect information
"""

def retrieve_relevant(user_message, k=4):
    """
    Retrieve relevant document chunks from FAISS.
    
    Args:
        user_message: User query
        k: Number of results to retrieve
    
    Returns:
        Formatted string with relevant sources and minimum distance
    """
    try:
        index, metadata = load_index()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return "No knowledge base found.", 1.0
    
    # Generate query embedding
    q_emb = embedder.embed_query(user_message)
    q_emb_array = np.array([q_emb], dtype='float32')
    
    # Search FAISS index
    distances, indices = index.search(q_emb_array, k)
    
    # Format results
    pairs = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx < len(metadata["documents"]):
            doc = metadata["documents"][idx]
            meta = metadata["metadatas"][idx]
            # Convert distance to similarity score (higher is better)
            similarity = float(dist)  # FAISS returns inner product (already similarity for normalized vectors)
            pairs.append(f"Source (url={meta.get('url', 'unknown')}, relevance={similarity:.2f}):\n{doc}")
    
    retrieved_text = "\n\n".join(pairs)
    min_similarity = float(distances[0][0]) if len(distances[0]) > 0 else 0.0
    
    return retrieved_text, min_similarity

from bot import memory

def make_prompt(user_message, retrieved_text, history_text=""):
    """
    Construct prompt for WhatsApp-optimized conversational responses.
    """
    prompt = f"""
Customer question: "{user_message}"

Relevant information from our knowledge base:
{retrieved_text}

Previous conversation context:
{history_text}

Instructions:
- Provide a clear, accurate answer based on the information above
- Keep your response concise (2-3 short paragraphs maximum)
- Use a professional yet friendly tone
- If the information isn't in the knowledge base, politely let them know and offer to connect them with the team
- One emoji is acceptable if it feels natural, but don't overuse them
"""
    return prompt

def generate_reply(user_message, phone_number="unknown"):
    """
    Generate reply using RAG pipeline:
    1. Retrieve relevant documents
    2. Construct prompt with context AND history
    3. Call OpenAI
    4. Return response
    
    Args:
        user_message: User's WhatsApp message
        phone_number: User's phone number (key for memory)
    
    Returns:
        Generated response text
    """
    try:
        # Add User message to memory
        memory.add_message(phone_number, "user", user_message)
        
        # Get history
        history = memory.get_history(phone_number)

        retrieved, min_similarity = retrieve_relevant(user_message, k=4)
        
        # If similarity is too low, we still pass it to the LLM but with a warning (or just rely on the prompt)
        # We REMOVE the strict early return so that conversational context (Greeting, "My name is...") works.
        
        prompt = make_prompt(user_message, retrieved, history)
        resp = call_openai(SYSTEM_PROMPT, prompt)
        
        # Add Assistant response to memory
        memory.add_message(phone_number, "assistant", resp)
        
        return resp
    except Exception as e:
        print(f"Error generating reply: {e}")
        import traceback
        traceback.print_exc()
        return ("I apologize, but I'm having trouble processing your request right now. "
                "Please try again, or I can connect you with our team for immediate assistance.")
