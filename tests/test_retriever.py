from langchain_core.documents import Document

from app.services.retriever import retrieve_documents


def test_retrieve_documents_returns_list(prepared_vectorstore):
    results = retrieve_documents("registration")
    assert isinstance(results, list)


def test_retrieve_documents_not_empty_for_registration(prepared_vectorstore):
    results = retrieve_documents("registration")
    assert len(results) > 0


def test_retrieve_documents_finds_website_content(prepared_vectorstore):
    results = retrieve_documents("cybersecurity bootcamps")
    assert len(results) > 0
    # At least one result should originate from the website fixture
    sources = [doc.metadata.get("source_type") for doc in results]
    assert "website" in sources


def test_retrieve_documents_returns_langchain_documents(prepared_vectorstore):
    results = retrieve_documents("registration")
    for document in results:
        assert isinstance(document, Document)


def test_retrieve_documents_respects_k(prepared_vectorstore):
    k = 3
    results = retrieve_documents("registration", k=k)
    assert len(results) <= k


def test_retrieve_documents_filters_unrelated_query_with_threshold(prepared_vectorstore):
    # Unrelated queries with high distance scores get filtered out
    results = retrieve_documents("What is the exact population count of the Moon in 1842?")
    assert len(results) == 0

