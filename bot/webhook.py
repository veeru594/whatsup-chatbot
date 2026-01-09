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


# Security & Reliability
import hmac
import hashlib

async def verify_signature(request: Request):
    """
    Verify X-Hub-Signature-256 header.
    """
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        raise HTTPException(status_code=403, detail="Missing signature")
    
    body = await request.body()
    expected_signature = "sha256=" + hmac.new(
        settings.WHATSAPP_APP_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(status_code=403, detail="Invalid signature")

# Idempotency
PROCESSED_IDS = set()
MAX_PROCESSED_IDS = 1000

@app.post("/webhook")
async def webhook(request: Request):
    """
    Main webhook endpoint for receiving WhatsApp messages.
    Processes incoming messages and sends AI-generated replies.
    """
    # 1. Verify Signature
    await verify_signature(request)

    data = await request.json()
    
    # ... (logging skipped for brevity, keeping core logic clean) ...
    # Log incoming webhook data
    print("\n" + "="*60)
    print("📨 WEBHOOK RECEIVED")
    print("="*60)
    
    try:
        entries = data.get("entry", [])
        
        for entry in entries:
            changes = entry.get("changes", [])
            
            for change in changes:
                value = change.get("value", {})
                messages = value.get("messages", [])
                
                if not messages:
                    continue
                
                for msg in messages:
                    # 2. Idempotency Check
                    msg_id = msg.get("id")
                    if msg_id in PROCESSED_IDS:
                        print(f"⚠️  Skipping duplicate message ID: {msg_id}")
                        continue
                    
                    if msg_id:
                        PROCESSED_IDS.add(msg_id)
                        # Rotate if too large
                        if len(PROCESSED_IDS) > MAX_PROCESSED_IDS:
                            PROCESSED_IDS.pop()

                    phone = msg.get("from")
                    text = msg.get("text", {}).get("body")
                    
                    if not text:
                        print("   ⚠️  Skipping (no text body)")
                        continue
                    
                    print(f"\n🔍 Processing message: '{text}'")
                    print(f"🤖 Generating AI reply for {phone}...")
                    
                    # Generate AI reply
                    reply = generate_reply(text, phone)
                    
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
        # Do NOT raise exception here to avoid 500 error to WhatsApp (which causes infinite retries)
        # Just return 200 OK after logging error
    
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


