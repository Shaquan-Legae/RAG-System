from typing import Optional, Tuple

from app.services.llm import generate_response
from app.services.retriever import retrieve_documents
from app.utils.source_formatter import format_source

NOT_FOUND_MESSAGE = "I could not find that information in the available knowledge base."


def answer_question(question: str) -> Tuple[str, Optional[str]]:
    """Answer a question using retrieved context and Ollama, returning (answer, source)."""

    documents = retrieve_documents(question)

    if not documents:
        return NOT_FOUND_MESSAGE, None

    # Primary source is the top-ranked retrieved document
    primary_source = format_source(documents[0])

    context = "\n\n".join(document.page_content for document in documents)

    prompt = (
        "Answer the question directly in concise continuous text based only on the provided context below. "
        "Do not use bullet points or newline characters. "
        "Do not include conversational filler or assumed information. "
        f"If the answer cannot be found in the context, reply exactly with: \"{NOT_FOUND_MESSAGE}\"\n\n"
        f"Context:\n{context}\n\n"
        f"Question:\n{question}\n\n"
        "Answer:"
    )

    answer = generate_response(prompt).strip()

    if NOT_FOUND_MESSAGE.lower() in answer.lower():
        return NOT_FOUND_MESSAGE, None

    return answer, primary_source

