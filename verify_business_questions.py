
import sys
import os

# Ensure we can import from bot module
sys.path.append(os.getcwd())

from bot.responder import generate_reply

questions = [
    "What specific services does Yoi Media offer?",
    "Can you give me an overview of what Yoi Media does?",
    "Do you offer AI-powered content creation?",
    "Why should I choose Yoi Media over other agencies?",
    "Tell me about your intelligent automation services.",
    "How does your SEO service help my business?",
    "Do you provide AI chatbots for customer support?",
    "What distinguishes your approach to digital marketing?",
    "Do you offer paid advertising services?"
]


# Open file safely
with open("business_answers.txt", "w", encoding="utf-8") as f:
    f.write("="*60 + "\n")
    f.write("VERIFYING BUSINESS ANSWERS\n")
    f.write("="*60 + "\n")

    for i, q in enumerate(questions, 1):
        msg_q = f"\nQ{i}: {q}\n"
        print(msg_q.strip())
        f.write(msg_q)
        f.write("-" * 60 + "\n")
        try:
            ans = generate_reply(q)
            msg_a = f"A: {ans}\n"
            print(msg_a.strip())
            f.write(msg_a)
        except Exception as e:
            msg_e = f"ERROR: {e}\n"
            print(msg_e.strip())
            f.write(msg_e)
        f.write("=" * 60 + "\n")

