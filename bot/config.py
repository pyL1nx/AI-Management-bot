import os
from dotenv import load_dotenv

# Load .env for local dev; on Railway, Variables are injected into the environment
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Optional, but configurable from Railway too
GROQ_BASE_URL = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
GROQ_MODEL = os.getenv("GROQ_MODEL", "deepseek-r1-distill-llama-70b")

# Fail fast if required secrets are missing
if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN environment variable")
if not GROQ_API_KEY:
    raise RuntimeError("Missing GROQ_API_KEY environment variable")
