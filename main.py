# main.py
import uvicorn
from bot.webhook import app
from config.settings import settings

if __name__ == "__main__":
    print("🚀 Starting WhatsApp RAG Bot...")
    print(f"📍 Server will run on http://0.0.0.0:{settings.PORT}")
    print(f"🔗 Public webhook URL should be: {settings.HOST_URL}/webhook")
    
    uvicorn.run(
        "bot.webhook:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=False
    )
