from fastapi import APIRouter, HTTPException

from app.config import CHROMA_PATH
from app.models.request_models import QuestionRequest
from app.services.pdf_loader import load_handbook
from app.services.rag import answer_question
from app.services.text_splitter import split_documents
from app.services.vectorstore import create_vectorstore, load_vectorstore

router = APIRouter()


@router.get("/")
def get_root() -> dict[str, str]:
    """Return the API service status."""

    return {"service": "RAG API", "status": "running"}


@router.get("/health")
def get_health() -> dict[str, bool]:
    """Return the API health status."""

    return {"healthy": True}


@router.get("/chunks")
def get_chunks() -> dict[str, int]:
    """Return the number of indexed handbook chunks."""

    if not CHROMA_PATH.exists():
        return {"chunks": 0}

    vectorstore = load_vectorstore()
    number_of_chunks = vectorstore._collection.count()

    return {"chunks": number_of_chunks}


@router.post("/reload")
def reload_index() -> dict[str, str]:
    """Reload the handbook and rebuild the vector database."""

    try:
        documents = load_handbook()
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error

    chunks = split_documents(documents)
    create_vectorstore(chunks)

    return {"message": "Handbook reloaded successfully."}


@router.post("/ask")
def ask_question(request: QuestionRequest) -> dict[str, str]:
    """Answer a question using the RAG service."""

    answer = answer_question(request.question)

    return {"answer": answer}
