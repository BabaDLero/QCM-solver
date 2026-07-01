import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPCODE_API_KEY", "")
API_URL = os.getenv("OPCODE_API_URL", "https://opencode.ai/zen/v1/chat/completions")
MODEL = "deepseek-v4-flash-free"
TRIGGER_KEY = "*"
OVERLAY_WIDTH = 400
OVERLAY_HEIGHT = 200
LOG_FILE = "app.log"
