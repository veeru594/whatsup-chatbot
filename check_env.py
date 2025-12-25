# check_env.py
"""
Check .env configuration and provide clear error messages.
"""

import os
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has required variables."""
    
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ .env file not found!")
        print("\n Create it by copying .env.example:")
        print("   copy .env.example .env")
        return False
    
    print("✓ .env file found")
    
    # Read .env content
    content = env_file.read_text()
    lines = content.split('\n')
    
    # Check for required Groq variables
    required = {
        "GROQ_API_KEY": False,
        "LLM_MODEL": False,
        "SITEMAP_URL": False,
        "WHATSAPP_TOKEN": False,
        "WHATSAPP_PHONE_ID": False,
    }
    
    print("\n📋 Checking required variables:")
    print("-" * 50)
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            if '=' in line:
                key = line.split('=')[0].strip()
                value = line.split('=', 1)[1].strip()
                
                if key in required:
                    required[key] = True
                    # Check if it's a placeholder
                    is_placeholder = (
                        'your-' in value.lower() or
                        'xxx' in value.lower() or
                        'example' in value.lower() or
                        len(value) < 3
                    )
                    
                    if is_placeholder:
                        print(f"⚠️  {key}: placeholder value (needs update)")
                    else:
                        print(f"✓  {key}: configured ({value[:20]}...)")
    
    # Check for OLD OpenAI key (should be removed)
    if "OPENAI_API_KEY" in content:
        print(f"\n⚠️  WARNING: Found OPENAI_API_KEY in .env")
        print("   This is no longer needed. We're using GROQ_API_KEY now.")
        print("   Either remove the OPENAI_API_KEY line or it will cause pydantic errors.")
    
    # Report missing variables
    missing = [k for k, v in required.items() if not v]
    if missing:
        print(f"\n❌ Missing variables: {', '.join(missing)}")
        return False
    
    print("\n✅ All required variables present!")
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("Environment Configuration Check")
    print("=" * 50)
    check_env_file()
