import re
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

from app.config import HANDBOOK_PATH


def _normalize_text(text: str) -> str:
    """Convert spaced-out PDF text into readable words."""

    text = re.sub(
        r"\b(?:[A-Za-z0-9] ){1,}[A-Za-z0-9]\b",
        lambda match: match.group().replace(" ", ""),
        text,
    )
    text = re.sub(r" {2,}", " ", text)

    return text


def load_handbook() -> List[Document]:
    """Load the handbook PDF and return its pages as LangChain Documents."""

    if not HANDBOOK_PATH.exists():
        raise FileNotFoundError(f"Handbook not found: {HANDBOOK_PATH}")

    loader = PyPDFLoader(str(HANDBOOK_PATH))
    documents = loader.load()

    for document in documents:
        document.page_content = _normalize_text(document.page_content)
        page_num = document.metadata.get("page", 0) + 1
        document.metadata = {
            "source_type": "handbook",
            "source_name": "Student Handbook",
            "page": page_num,
        }

    return documents
