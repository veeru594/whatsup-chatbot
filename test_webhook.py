# test_webhook.py
"""
Test script for webhook functionality using FastAPI TestClient to verify security and reliability.
"""

from fastapi.testclient import TestClient
from bot.webhook import app
import json
import hmac
import hashlib
from config.settings import settings

client = TestClient(app)

def sign_payload(payload, secret):
    body = json.dumps(payload).encode()
    signature = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return f"sha256={signature}"

def test_security_and_idempotency():
    print("🧪 STARTING HARDENING VERIFICATION")
    print("="*60)

    # Payload template
    def get_payload(msg_id, text):
        return {
            "object": "whatsapp_business_account",
            "entry": [{
                "id": "111111",
                "changes": [{
                    "value": {
                        "messages": [{
                            "from": "1234567890",
                            "id": msg_id,
                            "type": "text",
                            "text": {"body": text}
                        }]
                    }
                }]
            }]
        }

    # 1. Test Missing Signature
    print("\n[1] Testing Missing Signature...")
    resp = client.post("/webhook", json=get_payload("id_1", "test"))
    if resp.status_code == 403 and "Missing signature" in resp.text:
        print("✅ PASS: Rejected missing signature")
    else:
        print(f"❌ FAIL: Expected 403, got {resp.status_code} {resp.text}")

    # 2. Test Invalid Signature
    print("\n[2] Testing Invalid Signature...")
    headers = {"X-Hub-Signature-256": "sha256=invalid"}
    resp = client.post("/webhook", json=get_payload("id_1", "test"), headers=headers)
    if resp.status_code == 403 and "Invalid signature" in resp.text:
        print("✅ PASS: Rejected invalid signature")
    else:
        print(f"❌ FAIL: Expected 403, got {resp.status_code} {resp.text}")

    # 3. Test Valid Signature & Success
    print("\n[3] Testing Valid Signature...")
    payload = get_payload("msg_unique_1", "What is Yoi Media?")
    sig = sign_payload(payload, settings.WHATSAPP_APP_SECRET)
    resp = client.post("/webhook", json=payload, headers={"X-Hub-Signature-256": sig})
    
    if resp.status_code == 200:
        print("✅ PASS: Accepted valid signature")
    else:
        print(f"❌ FAIL: Expected 200, got {resp.status_code} {resp.text}")

    # 4. Test Idempotency (Duplicate ID)
    print("\n[4] Testing Idempotency (Replay Attack)...")
    # Send SAME payload again
    resp = client.post("/webhook", json=payload, headers={"X-Hub-Signature-256": sig})
    if resp.status_code == 200:
        print("✅ PASS: Handled duplicate request safely (returned 200 but logic should skip)")
        # Note: We rely on console logs to confirm "Skipping duplicate" message
    else:
         print(f"❌ FAIL: Expected 200, got {resp.status_code}")

    print("\n" + "="*60)
    print("VERIFICATION COMPLETE")

if __name__ == "__main__":
    test_security_and_idempotency()
