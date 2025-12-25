import requests
from config.settings import settings

GROQ_API = "https://api.groq.com/openai/v1/chat/completions"


def call_groq(system_prompt, user_prompt, temperature=0.2, max_tokens=512):
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": settings.LLM_MODEL,   # MUST be a valid Groq model
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "top_p": 1,
        "max_completion_tokens": max_tokens
    }

    resp = requests.post(GROQ_API, headers=headers, json=data, timeout=30)

    # DEBUG LOGGING – PRINT THE FULL ERROR BODY
    if resp.status_code != 200:
        print("\n==================== GROQ ERROR ====================")
        print("Status:", resp.status_code)
        print("Response:\n", resp.text)
        print("====================================================\n")

    resp.raise_for_status()  # This will now show full details

    j = resp.json()
    return j["choices"][0]["message"]["content"].strip()


call_openai = call_groq
