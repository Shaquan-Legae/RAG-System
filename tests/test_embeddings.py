from langchain_huggingface import HuggingFaceEmbeddings

from app.services.embeddings import get_embeddings


def test_get_embeddings_returns_embedding_model():
    embeddings = get_embeddings()
    assert isinstance(embeddings, HuggingFaceEmbeddings)


def test_get_embeddings_is_not_none():
    embeddings = get_embeddings()
    assert embeddings is not None


def test_get_embeddings_can_embed_sentence():
    embeddings = get_embeddings()
    vector = embeddings.embed_query("The university offers registration support.")
    assert isinstance(vector, list)
    assert len(vector) > 0
