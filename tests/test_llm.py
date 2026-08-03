import pytest
import ollama

from app.services.llm import generate_response


def _skip_if_ollama_unavailable():
    try:
        ollama.list()
    except Exception:
        pytest.skip("Ollama is not running. Start Ollama to run these tests.")


def test_generate_response_returns_string():
    _skip_if_ollama_unavailable()
    response = generate_response("Say hello in one sentence.")
    assert isinstance(response, str)


def test_generate_response_not_empty():
    _skip_if_ollama_unavailable()
    response = generate_response("Say hello in one sentence.")
    assert response.strip()


def test_generate_response_handles_empty_prompt():
    _skip_if_ollama_unavailable()
    response = generate_response("")
    assert isinstance(response, str)
