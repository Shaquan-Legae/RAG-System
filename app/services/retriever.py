from typing import List, Optional

from langchain_core.documents import Document

from app.config import SCORE_THRESHOLD
from app.services.vectorstore import load_vectorstore


def retrieve_documents(
    question: str,
    k: int = 5,
    score_threshold: Optional[float] = SCORE_THRESHOLD,
) -> List[Document]:
    """Retrieve the most relevant document chunks for a question."""

    vectorstore = load_vectorstore()

    if score_threshold is None:
        return vectorstore.similarity_search(question, k=k)

    results_with_scores = vectorstore.similarity_search_with_score(question, k=k)

    # In Chroma L2 distance, lower score indicates higher similarity
    documents = [
        doc for doc, score in results_with_scores if score <= score_threshold
    ]

    return documents

