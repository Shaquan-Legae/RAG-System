from app.services.llm import generate_response
from app.services.retriever import retrieve_documents

NOT_FOUND_MESSAGE = "I could not find that information in the handbook."


def answer_question(question: str) -> str:
    """Answer a question using retrieved handbook context and Ollama."""

    documents = retrieve_documents(question)

    if not documents:
        return NOT_FOUND_MESSAGE

    context = "\n\n".join(document.page_content for document in documents)

    prompt = (
        "You are an assistant answering questions about a university handbook.\n\n"
        "Use ONLY the information provided below.\n\n"
        "If the answer cannot be found in the context, reply:\n\n"
        f"\"{NOT_FOUND_MESSAGE}\"\n\n"
        "Context:\n\n"
        f"{context}\n\n"
        "Question:\n\n"
        f"{question}\n\n"
        "Answer:"
    )

    answer = generate_response(prompt)

    return answer
