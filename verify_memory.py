
import sys
import os
sys.path.append(os.getcwd())
from bot.responder import generate_reply

def test_memory():
    phone = "1234567890"
    
    print("Turn 1: User says 'My name is Alice'")
    reply1 = generate_reply("My name is Alice, and I am the CEO of a bakery.", phone)
    print(f"Bot: {reply1}\n")
    
    print("Turn 2: User says 'What is my name and what do I do?'")
    reply2 = generate_reply("What is my name and what do I do?", phone)
    print(f"Bot: {reply2}\n")
    
    if "Alice" in reply2 and "bakery" in reply2.lower():
        print("✅ MEMORY TEST PASSED: Bot remembered name and job.")
    else:
        print("❌ MEMORY TEST FAILED: Bot did not mention 'Alice' or 'bakery'.")

if __name__ == "__main__":
    test_memory()
