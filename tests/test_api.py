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


@patch("app.api.routes.answer_question", return_value="Test answer")
def test_post_ask(mock_answer_question):
    response = client.post("/ask", json={"question": "Test question"})
    assert response.status_code == 200
    assert response.json() == {"answer": "Test answer"}
    mock_answer_question.assert_called_once_with("Test question")


def test_post_reload():
    response = client.post("/reload")
    assert response.status_code == 200
    assert response.json()["message"] == "Handbook reloaded successfully."


def test_get_chunks():
    response = client.get("/chunks")
    assert response.status_code == 200
    assert "chunks" in response.json()
