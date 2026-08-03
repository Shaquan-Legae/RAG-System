from typing import List

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.config import CHROMA_PATH
from app.services.embeddings import get_embeddings


def delete_vectorstore() -> None:
    """Remove the existing persistent Chroma database."""

    if CHROMA_PATH.exists():
        embeddings = get_embeddings()
        vectorstore = Chroma(
            persist_directory=str(CHROMA_PATH),
            embedding_function=embeddings,
        )
        vectorstore.delete_collection()


def create_vectorstore(chunks: List[Document]) -> Chroma:
    """Create a persistent Chroma database from document chunks."""

    embeddings = get_embeddings()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_PATH),
    )

    return vectorstore


def load_vectorstore() -> Chroma:
    """Load an existing Chroma database from disk."""

    embeddings = get_embeddings()

    vectorstore = Chroma(
        persist_directory=str(CHROMA_PATH),
        embedding_function=embeddings,
    )

    return vectorstore
