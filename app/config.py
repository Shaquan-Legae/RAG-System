from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

HANDBOOK_PATH = BASE_DIR / "handbook" / "handbook.pdf"

CHROMA_PATH = BASE_DIR / "chroma_db"

load_dotenv(BASE_DIR / ".env")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

CHUNK_SIZE = 500

CHUNK_OVERLAP = 100

ZAIO_URL = os.getenv("ZAIO_URL", "https://www.zaio.io")

SCORE_THRESHOLD = float(os.getenv("SCORE_THRESHOLD", "1.45"))