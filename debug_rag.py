from app.services.llm import generate_response
from app.services.rag import NOT_FOUND_MESSAGE
from app.services.retriever import retrieve_documents


QUESTION = "When does registration open?"


def main() -> None:
    """Print retrieval, prompt, and Ollama response details."""

    documents = retrieve_documents(QUESTION)

    print("========== Retrieved Documents ==========")
    print(f"Number of retrieved documents: {len(documents)}")

    for index, document in enumerate(documents, start=1):
        print(f"\nDocument {index} metadata: {document.metadata}")
        print(f"Document {index} content:\n{document.page_content[:500]}")

    context = "\n\n".join(document.page_content for document in documents)
    prompt = (
        "You are an assistant answering questions about a university handbook.\n\n"
        "Use ONLY the information provided below.\n\n"
        "If the answer cannot be found in the context, reply:\n\n"
        f"\"{NOT_FOUND_MESSAGE}\"\n\n"
        "Context:\n\n"
        f"{context}\n\n"
        "Question:\n\n"
        f"{QUESTION}\n\n"
        "Answer:"
    )

    print("\n========== Prompt ==========")
    print(prompt)

    answer = generate_response(prompt)

    print("\n========== Ollama Response ==========")
    print(answer)


if __name__ == "__main__":
    main()
