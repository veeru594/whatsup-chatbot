# bot/memory.py
from typing import List, Dict

# Global dictionary to store conversation history
# Structure: { "phone_number": [ {"role": "user/assistant", "content": "..."} ] }
HISTORY: Dict[str, List[Dict[str, str]]] = {}

MAX_HISTORY_LEN = 10  # Store last 10 messages (5 user + 5 assistant)

def add_message(phone: str, role: str, message: str):
    """
    Add a message to the user's history.
    
    Args:
        phone: User's phone number
        role: "user" or "assistant"
        message: Content of the message
    """
    if phone not in HISTORY:
        HISTORY[phone] = []
    
    HISTORY[phone].append({"role": role, "content": message})
    
    # Trim history if it exceeds limit
    if len(HISTORY[phone]) > MAX_HISTORY_LEN:
        HISTORY[phone] = HISTORY[phone][-MAX_HISTORY_LEN:]

def get_history(phone: str) -> str:
    """
    Retrieve formatted history for the prompt context.
    
    Args:
        phone: User's phone number
        
    Returns:
        String formatted as:
        User: ...
        Assistant: ...
    """
    if phone not in HISTORY or not HISTORY[phone]:
        return ""
    
    formatted_history = []
    for msg in HISTORY[phone]:
        role_label = "User" if msg["role"] == "user" else "Assistant"
        formatted_history.append(f"{role_label}: {msg['content']}")
        
    return "\n".join(formatted_history)
