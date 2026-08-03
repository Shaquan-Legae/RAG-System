from pydantic import BaseModel


class QuestionRequest(BaseModel):
    """Request body for a handbook question."""

    question: str
