from typing import List

from langchain_core.documents import Document

from app.services.vectorstore import load_vectorstore


def retrieve_documents(question: str, k: int = 5) -> List[Document]:
    """Retrieve the most relevant document chunks for a question."""

    vectorstore = load_vectorstore()
    documents = vectorstore.similarity_search(question, k=k)

    return documents
