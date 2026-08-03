from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

from app.config import HANDBOOK_PATH


def load_handbook() -> List[Document]:
    """Load the handbook PDF and return its pages as LangChain Documents."""

    if not HANDBOOK_PATH.exists():
        raise FileNotFoundError(f"Handbook not found: {HANDBOOK_PATH}")

    loader = PyPDFLoader(str(HANDBOOK_PATH))
    documents = loader.load()

    return documents
