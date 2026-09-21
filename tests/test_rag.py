from unittest.mock import patch

import pytest
import ollama
from langchain_core.documents import Document

from app.services.rag import NOT_FOUND_MESSAGE, answer_question


def _ollama_is_available() -> bool:
    """Return whether Ollama is available for integration tests."""
    try:
        ollama.list()
    except Exception:
        return False
    return True


OLLAMA_AVAILABLE = _ollama_is_available()


@pytest.mark.skipif(
    not OLLAMA_AVAILABLE,
    reason="Ollama is not running. Start Ollama to run these tests.",
)
def test_answer_question_returns_tuple(prepared_vectorstore):
    answer, source = answer_question("When does registration open?")
    assert isinstance(answer, str)
    assert source is None or isinstance(source, str)


@pytest.mark.skipif(
    not OLLAMA_AVAILABLE,
    reason="Ollama is not running. Start Ollama to run these tests.",
)
def test_answer_question_returns_non_empty_for_known_question(prepared_vectorstore):
    answer, source = answer_question("When does registration open?")
    assert answer.strip()


@pytest.mark.skipif(
    not OLLAMA_AVAILABLE,
    reason="Ollama is not running. Start Ollama to run these tests.",
)
def test_answer_question_handles_unrelated_question(prepared_vectorstore):
    answer, source = answer_question("What is the capital of Mars?")
    assert isinstance(answer, str)


@patch("app.services.rag.retrieve_documents", return_value=[])
def test_answer_question_no_documents(mock_retrieve):
    answer, source = answer_question("When does registration open?")
    assert answer == NOT_FOUND_MESSAGE
    assert source is None


@patch("app.services.rag.generate_response", return_value="Zaio offers Fullstack AI Engineer Bootcamps.")
@patch("app.services.rag.retrieve_documents")
def test_answer_question_website_source(mock_retrieve, mock_generate):
    mock_retrieve.return_value = [
        Document(
            page_content="Zaio courses overview",
            metadata={"source_type": "website", "url": "https://www.zaio.io/bootcamps"},
        )
    ]
    answer, source = answer_question("What courses does ZAIO offer?")
    assert "Fullstack AI Engineer" in answer
    assert source == "https://www.zaio.io/bootcamps"


@patch("app.services.rag.generate_response", return_value="Attendance is mandatory for all live sessions.")
@patch("app.services.rag.retrieve_documents")
def test_answer_question_handbook_source(mock_retrieve, mock_generate):
    mock_retrieve.return_value = [
        Document(
            page_content="Attendance policy details",
            metadata={"source_type": "handbook", "source_name": "Student Handbook", "page": 10},
        )
    ]
    answer, source = answer_question("What is the attendance requirement?")
    assert "Attendance is mandatory" in answer
    assert source == "Student Handbook - Page 10"


@patch("app.services.rag.generate_response", return_value=NOT_FOUND_MESSAGE)
@patch("app.services.rag.retrieve_documents")
def test_answer_question_llm_fallback(mock_retrieve, mock_generate):
    mock_retrieve.return_value = [
        Document(
            page_content="Some general context",
            metadata={"source_type": "handbook", "page": 1},
        )
    ]
    answer, source = answer_question("What is the population of Japan?")
    assert answer == NOT_FOUND_MESSAGE
    assert source is None

