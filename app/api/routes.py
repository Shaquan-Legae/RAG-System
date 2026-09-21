from fastapi import APIRouter, HTTPException

from app.config import CHROMA_PATH
from app.models.request_models import QuestionRequest, QuestionResponse
from app.services.pdf_loader import load_handbook
from app.services.rag import answer_question
from app.services.text_splitter import split_documents
from app.services.vectorstore import (
    create_vectorstore,
    delete_vectorstore,
    load_vectorstore,
)
from app.services.website_loader import load_website

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
    """Return the total number of indexed document chunks."""

    if not CHROMA_PATH.exists():
        return {"chunks": 0}

    vectorstore = load_vectorstore()
    number_of_chunks = vectorstore._collection.count()

    return {"chunks": number_of_chunks}


@router.post("/reload")
def reload_index() -> dict[str, str]:
    """Reload both the handbook and ZAIO website and rebuild the vector database."""

    all_documents = []

    # 1. Load Student Handbook PDF
    try:
        handbook_docs = load_handbook()
        all_documents.extend(handbook_docs)
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error

    # 2. Load ZAIO Website
    try:
        website_docs = load_website()
        all_documents.extend(website_docs)
    except Exception as error:
        # Continue with handbook if website crawling encounters network issue
        pass

    chunks = split_documents(all_documents)
    delete_vectorstore()
    create_vectorstore(chunks)

    return {"message": "Knowledge base reloaded successfully (Handbook + ZAIO Website)."}


@router.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest) -> QuestionResponse:
    """Answer a question using the RAG service and return answer with source."""

    try:
        answer, source = answer_question(request.question)
    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail=f"LLM generation service unavailable: {error}",
        ) from error

    return QuestionResponse(answer=answer, source=source)


