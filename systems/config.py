import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

OWNER_ID = int(os.getenv("OWNER_ID", "0"))

PREFIX = "$"

OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "qwen3:1.7b"
