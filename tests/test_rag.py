from unittest.mock import patch

import pytest
import ollama

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
def test_answer_question_returns_string(prepared_vectorstore):
    answer = answer_question("When does registration open?")
    assert isinstance(answer, str)


@pytest.mark.skipif(
    not OLLAMA_AVAILABLE,
    reason="Ollama is not running. Start Ollama to run these tests.",
)
def test_answer_question_returns_non_empty_for_known_question(prepared_vectorstore):
    answer = answer_question("When does registration open?")
    assert answer.strip()


@pytest.mark.skipif(
    not OLLAMA_AVAILABLE,
    reason="Ollama is not running. Start Ollama to run these tests.",
)
def test_answer_question_handles_unrelated_question(prepared_vectorstore):
    answer = answer_question("What is the capital of Mars?")
    assert isinstance(answer, str)


@patch("app.services.rag.retrieve_documents", return_value=[])
def test_answer_question_no_documents(mock_retrieve):
    answer = answer_question("When does registration open?")
    assert answer == NOT_FOUND_MESSAGE
