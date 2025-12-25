# test_webhook.py
"""
Test script for webhook functionality without using WhatsApp.
Run this after starting the server to test the RAG pipeline.
"""

import requests
import json

def test_webhook():
    """Test the webhook endpoint with a sample message."""
    
    url = "http://localhost:8000/webhook"
    
    # Sample WhatsApp webhook payload (matches real WhatsApp Cloud API structure)
    payload = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "111111",
                "changes": [
                    {
                        "field": "messages",
                        "value": {
                            "messaging_product": "whatsapp",
                            "contacts": [
                                {"profile": {"name": "Veeru"}, "wa_id": "1234567890"}
                            ],
                            "messages": [
                                {
                                    "from": "1234567890",
                                    "id": "wamid.HBgXXXXXX",
                                    "timestamp": "1234567890",
                                    "text": {"body": "What services do you offer?"},
                                    "type": "text"
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }
    
    print("🧪 Testing webhook endpoint...")
    print(f"📤 Sending test message: {payload['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']}")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"\n✓ Status: {response.status_code}")
        print(f"✓ Response: {response.json()}")
        
        if response.status_code == 200:
            print("\n✅ Webhook test PASSED!")
            print("Check the server terminal for the AI-generated response.")
        else:
            print("\n❌ Webhook test FAILED!")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection failed! Make sure the server is running:")
        print("   python main.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    test_webhook()
