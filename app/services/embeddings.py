from langchain_huggingface import HuggingFaceEmbeddings

from app.config import EMBEDDING_MODEL


def get_embeddings() -> HuggingFaceEmbeddings:
    """Load and return the HuggingFace embedding model."""

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    return embeddings
