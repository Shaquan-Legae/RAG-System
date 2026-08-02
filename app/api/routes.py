from fastapi import APIRouter

router = APIRouter()


@router.post("/ask")
def ask_question():
    """Placeholder endpoint for asking a question."""
    return {"message": "Ask endpoint placeholder"}


@router.post("/reload")
def reload_index():
    """Placeholder endpoint for reloading the document index."""
    return {"message": "Reload endpoint placeholder"}


@router.get("/chunks")
def get_chunks():
    """Placeholder endpoint for returning document chunks."""
    return {"message": "Chunks endpoint placeholder"}
