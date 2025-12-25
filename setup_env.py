# setup_env.py
"""
Helper script to create .env file from template and validate configuration.
"""

import os
from pathlib import Path

def create_env_file():
    """Create .env file from .env.example if it doesn't exist."""
    
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_file.exists():
        print("✓ .env file already exists")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Keeping existing .env file")
            return
    
    if not env_example.exists():
        print("❌ .env.example not found!")
        return
    
    # Copy template
    content = env_example.read_text()
    env_file.write_text(content)
    
    print("\n✅ Created .env file from template")
    print("\n⚠️  IMPORTANT: Edit .env and add your actual credentials:")
    print("   - OPENAI_API_KEY")
    print("   - WHATSAPP_TOKEN")
    print("   - WHATSAPP_PHONE_ID")
    print("   - WHATSAPP_VERIFY_TOKEN")
    print("   - SITEMAP_URL")
    print("\n📝 Open .env in your editor and fill in the values.")

def validate_env():
    """Check if required environment variables are set."""
    
    required = [
        "OPENAI_API_KEY",
        "WHATSAPP_TOKEN",
        "WHATSAPP_PHONE_ID",
        "SITEMAP_URL"
    ]
    
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found! Run this script first to create it.")
        return False
    
    # Simple validation (not loading actual env)
    content = env_file.read_text()
    
    missing = []
    for var in required:
        if f"{var}=your-" in content or f"{var}=sk-your-" in content:
            missing.append(var)
    
    if missing:
        print("\n⚠️  The following variables need to be updated in .env:")
        for var in missing:
            print(f"   - {var}")
        return False
    
    print("\n✅ Environment configuration looks good!")
    return True

if __name__ == "__main__":
    print("🔧 WhatsApp RAG Bot - Environment Setup\n")
    create_env_file()
    print("\n" + "="*50)
    validate_env()
