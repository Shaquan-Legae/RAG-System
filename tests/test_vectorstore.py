from langchain_chroma import Chroma

from app.config import CHROMA_PATH
from app.services.pdf_loader import load_handbook
from app.services.text_splitter import split_documents
from app.services.vectorstore import create_vectorstore, load_vectorstore


def test_create_vectorstore_returns_chroma():
    documents = load_handbook()
    chunks = split_documents(documents)
    vectorstore = create_vectorstore(chunks)
    assert isinstance(vectorstore, Chroma)


def test_create_vectorstore_successfully_created():
    documents = load_handbook()
    chunks = split_documents(documents)
    vectorstore = create_vectorstore(chunks)
    assert vectorstore is not None


def test_chroma_directory_exists_after_creation():
    documents = load_handbook()
    chunks = split_documents(documents)
    create_vectorstore(chunks)
    assert CHROMA_PATH.exists()
    assert CHROMA_PATH.is_dir()


def test_load_vectorstore_returns_chroma():
    documents = load_handbook()
    chunks = split_documents(documents)
    create_vectorstore(chunks)
    vectorstore = load_vectorstore()
    assert isinstance(vectorstore, Chroma)


def test_similarity_search_registration():
    documents = load_handbook()
    chunks = split_documents(documents)
    create_vectorstore(chunks)
    vectorstore = load_vectorstore()
    results = vectorstore.similarity_search("registration")
    assert len(results) >= 1
