# bot/webhook.py
from fastapi import FastAPI, Request, HTTPException
from config.settings import settings
from bot.responder import generate_reply
import requests
import os

app = FastAPI()

from fastapi import Response

@app.get("/")
async def root_verify(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    print("ROOT VERIFY CALLED", dict(request.query_params))

    if mode == "subscribe" and token == settings.WHATSAPP_VERIFY_TOKEN:
        return Response(content=str(challenge), media_type="text/plain")

    return Response(content="OK", media_type="text/plain")

@app.get("/webhook")
async def verify(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    print("WEBHOOK VERIFY CALLED", dict(request.query_params))

    if mode == "subscribe" and token == settings.WHATSAPP_VERIFY_TOKEN:
        return Response(content=str(challenge), media_type="text/plain")

    return Response(content="Verification failed", status_code=403)

@app.post("/webhook")
async def webhook(request: Request):
    """
    Main webhook endpoint for receiving WhatsApp messages.
    Processes incoming messages and sends AI-generated replies.
    """
    data = await request.json()
    
    # Log incoming webhook data
    print("\n" + "="*60)
    print("📨 WEBHOOK RECEIVED")
    print("="*60)
    print(f"Raw data keys: {list(data.keys())}")
    print()
    
    try:
        entries = data.get("entry", [])
        print(f"Found {len(entries)} entries")
        
        for entry in entries:
            changes = entry.get("changes", [])
            print(f"Found {len(changes)} changes in entry")
            
            for change in changes:
                value = change.get("value", {})
                messages = value.get("messages", [])
                print(f"Found {len(messages)} messages in value")
                
                if not messages:
                    print("⚠️  No messages found in this change")
                    continue
                
                for msg in messages:
                    phone = msg.get("from")
                    text = msg.get("text", {}).get("body")
                    msg_type = msg.get("type")
                    
                    print(f"\n📱 Message details:")
                    print(f"   From: {phone}")
                    print(f"   Type: {msg_type}")
                    print(f"   Body: {text}")
                    
                    if not text:
                        print("   ⚠️  Skipping (no text body)")
                        continue
                    
                    print(f"\n🔍 Processing message: '{text}'")
                    print("🤖 Generating AI reply...")
                    
                    # Generate AI reply
                    reply = generate_reply(text)
                    
                    print(f"\n✅ Generated reply:")
                    print(f"   {reply[:200]}..." if len(reply) > 200 else f"   {reply}")
                    
                    # Send reply via WhatsApp
                    print(f"\n📤 Sending to {phone}...")
                    send_whatsapp_text(phone, reply)
                    
        print("\n" + "="*60)
        print("✅ WEBHOOK PROCESSING COMPLETE")
        print("="*60 + "\n")
                    
    except Exception as e:
        print(f"\n❌ WEBHOOK ERROR: {e}")
        import traceback
        traceback.print_exc()
        print()
    
    return {"status": "ok"}

def send_whatsapp_text(to_number, message):
    """
    Send text message via WhatsApp Cloud API.
    
    Args:
        to_number: Recipient's phone number
        message: Message text to send
    
    Returns:
        API response JSON
    """
    url = f"{settings.WHATSAPP_API_URL}/{settings.WHATSAPP_PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message}
    }
    
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        print(f"✓ Message sent to {to_number}")
        return resp.json()
    except Exception as e:
        print(f"✗ WhatsApp send failed: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return {"error": str(e)}


