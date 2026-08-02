from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

HANDBOOK_PATH = BASE_DIR / "handbook" / "handbook.pdf"

CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

OLLAMA_MODEL = "llama3.2"

CHUNK_SIZE = 500

CHUNK_OVERLAP = 100