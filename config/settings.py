# config/settings.py
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    GROQ_API_KEY: str
    LLM_MODEL: str = "llama-3.1-70b-versatile"
    WHATSAPP_TOKEN: str
    WHATSAPP_PHONE_ID: str
    WHATSAPP_VERIFY_TOKEN: str = "verify_token_val"
    WHATSAPP_API_URL: str = "https://graph.facebook.com/v16.0"
    CHROMA_DIR: str = "./chroma_db"
    EMBED_MODEL: str = "all-MiniLM-L6-v2"
    SITEMAP_URL: str
    SCRAPE_USER_AGENT: str = "MyBot/1.0"
    HOST_URL: str
    PORT: int = 8000
    MAX_CHUNK_TOKENS: int = 450

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields like old OPENAI_API_KEY

settings = Settings()
