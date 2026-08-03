import pytest

from app.services.pdf_loader import load_handbook
from app.services.text_splitter import split_documents
from app.services.vectorstore import create_vectorstore


@pytest.fixture(scope="module")
def prepared_vectorstore():
    # Module scope builds the vector database once for all retriever tests.
    # These tests only read from Chroma, so rebuilding it before every test
    # would be slow and unnecessary.
    documents = load_handbook()
    chunks = split_documents(documents)
    vectorstore = create_vectorstore(chunks)
    return vectorstore
