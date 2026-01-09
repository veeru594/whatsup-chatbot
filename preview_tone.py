"""
Simple tone test - just testing the prompt generation without API calls
"""
import sys
import os
sys.path.append(os.getcwd())

# Let's just show what the new prompts look like
print("=" * 70)
print(" 🧪 NEW WHATSAPP TONE - PROMPT PREVIEW")
print("=" * 70)

# Show the new system prompt
print("\n📋 NEW SYSTEM PROMPT (Bot's Personality):")
print("-" * 70)
print("""
You're a friendly assistant chatting on WhatsApp.

Your vibe:
- Sound like a real person - warm, helpful, casual but professional
- Use simple, clear language (no corporate jargon)
- Keep it brief - people are on their phones
- Use emojis naturally when it feels right (1-2 max, don't overdo it)
- Be direct and conversational

Golden rule:
Only share info from the sources provided. If you don't know something, 
be honest and offer to connect them with the team.

Avoid:
- Making up information or guessing
- Pricing/legal/medical advice  
- Long paragraphs (keep messages short and scannable)
- Being overly formal or robotic
""")

print("\n" + "=" * 70)
print("\n📱 EXAMPLE USER PROMPT STRUCTURE:")
print("-" * 70)
user_question = "What services do you offer?"
example_context = "[Retrieved website content about services...]"

print(f"""
Someone on WhatsApp asked: "{user_question}"

Here's what I found from our website:
{example_context}

Reply guidelines:
- Sound like you're chatting with a friend, not sending a corporate email
- Keep it SHORT - max 2-3 brief paragraphs (mobile screens!)
- Use line breaks for easy reading
- Add an emoji if it feels natural (1-2 max)
- If the info isn't there, just be honest and offer to connect them with the team
- Be helpful and genuine
""")

print("\n" + "=" * 70)
print("\n💬 NEW FALLBACK MESSAGES:")
print("-" * 70)
print("\n🔸 Low Confidence Response:")
print("   'Hmm, I don't have specific info on that in my knowledge base.")
print("    Want me to connect you with the team? They can help you out! 😊'")

print("\n🔸 Error Response:")
print("   'Oops, something went wrong on my end 😅")
print("    Could you try asking again? If it keeps happening, I'll get you to the team!'")

print("\n" + "=" * 70)
print("\n✅ TONE COMPARISON:")
print("-" * 70)
print("\n❌ OLD (Corporate & Robotic):")
print('   "I\'m not sure I have the right information to answer that."')
print('   "Would you like me to connect you with a human support agent?"')
print('   "Please share your email or phone number."')

print("\n✅ NEW (Human & Conversational):")
print('   "Hmm, I don\'t have specific info on that in my knowledge base."')
print('   "Want me to connect you with the team? They can help you out! 😊"')

print("\n" + "=" * 70)
print("\n🎯 The bot will now sound more like a helpful friend texting you")
print("   instead of a corporate support system!")
print("=" * 70)
