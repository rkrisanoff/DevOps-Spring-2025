import pytest
from litestar.testing import TestClient
from embedder.server import create_server


@pytest.fixture
def client():
    app = create_server()
    return TestClient(app)


def test_version_endpoint(client):
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": "0.4.0"}


def test_embeddings_endpoint(client):
    test_sentences = ["Hello world", "Test sentence"]
    response = client.get(
        "/api/v1/infer/embedding", params={"sentences": test_sentences}
    )
    assert response.status_code == 200

    embeddings = response.json()
    assert isinstance(embeddings, list)
    assert len(embeddings) == len(test_sentences)
    assert all(isinstance(emb, list) for emb in embeddings)
    assert all(isinstance(val, float) for emb in embeddings for val in emb)


def test_embeddings_empty_input(client):
    response = client.get("/api/v1/infer/embedding", params={"sentences": []})
    assert response.status_code == 400  # Empty list is not allowed
    assert "Missing required query parameter" in response.json()["detail"]


def test_embeddings_single_string(client):
    response = client.get(
        "/api/v1/infer/embedding", params={"sentences": "single string"}
    )
    assert response.status_code == 200
    embeddings = response.json()
    assert isinstance(embeddings, list)
    assert len(embeddings) == 1
    assert all(isinstance(val, float) for val in embeddings[0])
