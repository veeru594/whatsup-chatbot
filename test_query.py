# test_query.py
"""
Test querying the FAISS vector database.
"""

from bot.responder import generate_reply

def test_queries():
    """Test the RAG pipeline with sample queries."""
    
    test_questions = [
        "What services do you offer?",
        "What are your office hours?",
        "How can I contact you?",
        "Tell me about your experience",
    ]
    
    print("=" * 60)
    print("Testing Query System")
    print("=" * 60)
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        print("-" * 60)
        try:
            reply = generate_reply(question)
            print(f"🤖 Reply:\n{reply}")
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        print()

if __name__ == "__main__":
    test_queries()
