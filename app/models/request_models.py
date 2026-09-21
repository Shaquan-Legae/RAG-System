from typing import Optional
from pydantic import BaseModel


class QuestionRequest(BaseModel):
    """Request body for a question query."""

    question: str


class QuestionResponse(BaseModel):
    """Response body containing the generated answer and source attribution."""

    answer: str
    source: Optional[str] = None
