from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "service" in response.json()
    assert "status" in response.json()


def test_get_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["healthy"] is True


@patch("app.api.routes.answer_question", return_value=("Test answer", "https://www.zaio.io"))
def test_post_ask_returns_answer_and_source(mock_answer_question):
    response = client.post("/ask", json={"question": "Test question"})
    assert response.status_code == 200
    assert response.json() == {
        "answer": "Test answer",
        "source": "https://www.zaio.io",
    }
    mock_answer_question.assert_called_once_with("Test question")


def test_post_ask_invalid_request():
    response = client.post("/ask", json={"wrong_key": "No question"})
    assert response.status_code == 422


@patch("app.api.routes.load_website", return_value=[])
@patch("app.api.routes.load_handbook", return_value=[])
@patch("app.api.routes.create_vectorstore")
@patch("app.api.routes.delete_vectorstore")
def test_post_reload(mock_delete, mock_create, mock_handbook, mock_website):
    response = client.post("/reload")
    assert response.status_code == 200
    assert "Knowledge base reloaded successfully" in response.json()["message"]
    mock_handbook.assert_called_once()
    mock_website.assert_called_once()


def test_get_chunks():
    response = client.get("/chunks")
    assert response.status_code == 200
    assert "chunks" in response.json()

