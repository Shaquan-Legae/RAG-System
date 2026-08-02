from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "RAG API root"}


def test_get_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_post_ask():
    response = client.post("/ask")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "message" in response.json()


def test_post_reload():
    response = client.post("/reload")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "message" in response.json()


def test_get_chunks():
    response = client.get("/chunks")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "message" in response.json()
