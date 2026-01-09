
import sys
import os
sys.path.append(os.getcwd())
from bot.responder import generate_reply
import traceback

print("Debugging Q4...")
try:
    ans = generate_reply("Why should I choose Yoi Media over other agencies?")
    print("Answer:", ans)
except Exception:
    traceback.print_exc()
