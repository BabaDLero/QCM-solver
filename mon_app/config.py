import os
import sys
from dotenv import load_dotenv

if getattr(sys, 'frozen', False):
    _base_dir = os.path.dirname(sys.executable)
else:
    _base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(_base_dir, '.env'))

API_KEY = os.getenv("OPCODE_API_KEY", "")
API_URL = os.getenv("OPCODE_API_URL", "https://opencode.ai/zen/v1/chat/completions")
MODEL = "deepseek-v4-flash"
TRIGGER_KEY = "*"
OVERLAY_WIDTH = 400
OVERLAY_HEIGHT = 200
LOG_FILE = "app.log"
API_TIMEOUT = 30
API_MAX_TOKENS = 300
AUTO_HIDE_SECONDS = 8
DEBOUNCE_SECONDS = 2.0
