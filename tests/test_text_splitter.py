from app.services.pdf_loader import load_handbook
from app.services.text_splitter import split_documents


def test_split_documents_returns_list():
    documents = load_handbook()
    chunks = split_documents(documents)
    assert isinstance(chunks, list)


def test_split_documents_list_not_empty():
    documents = load_handbook()
    chunks = split_documents(documents)
    assert len(chunks) > 0


def test_split_documents_creates_at_least_as_many_chunks_as_documents():
    documents = load_handbook()
    chunks = split_documents(documents)
    assert len(chunks) >= len(documents)


def test_every_chunk_contains_text():
    documents = load_handbook()
    chunks = split_documents(documents)
    for chunk in chunks:
        assert chunk.page_content.strip()


def test_split_documents_works_with_load_handbook():
    documents = load_handbook()
    chunks = split_documents(documents)
    assert len(documents) > 0
    assert len(chunks) > 0
