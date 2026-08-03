from langchain_core.documents import Document

from app.services.retriever import retrieve_documents


def test_retrieve_documents_returns_list(prepared_vectorstore):
    results = retrieve_documents("registration")
    assert isinstance(results, list)


def test_retrieve_documents_not_empty_for_registration(prepared_vectorstore):
    results = retrieve_documents("registration")
    assert len(results) > 0


def test_retrieve_documents_returns_langchain_documents(prepared_vectorstore):
    results = retrieve_documents("registration")
    for document in results:
        assert isinstance(document, Document)


def test_retrieve_documents_respects_k(prepared_vectorstore):
    k = 3
    results = retrieve_documents("registration", k=k)
    assert len(results) <= k


def test_retrieve_documents_handles_unrelated_query(prepared_vectorstore):
    results = retrieve_documents("quantum physics black holes")
    assert isinstance(results, list)
