import sys
import os
import time

# Ensure we can import from bot module
sys.path.append(os.getcwd())

from bot.responder import generate_reply

# Test with a few questions to see the new tone
test_questions = [
    "What services do you offer?",
    "Tell me about your company",
    "How much does it cost?"  # This might trigger low-confidence response
]

print("=" * 70)
print(" 🧪 TESTING NEW WHATSAPP TONE")
print("=" * 70)
print("\nLet's see how the bot sounds with the new conversational style!\n")

for i, question in enumerate(test_questions, 1):
    print("\n" + "-" * 70)
    print(f"📱 Question {i}: {question}")
    print("-" * 70)
    
    try:
        # Add small delay to avoid hitting rate limits too hard
        if i > 1:
            time.sleep(2)
        
        answer = generate_reply(question)
        print(f"\n🤖 Bot Response:\n")
        print(answer)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    print("\n" + "=" * 70)

print("\n✅ Test complete! Check out the new tone above.")
print("=" * 70)
