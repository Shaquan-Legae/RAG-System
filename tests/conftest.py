import pytest
from langchain_core.documents import Document

from app.services.pdf_loader import load_handbook
from app.services.text_splitter import split_documents
from app.services.vectorstore import create_vectorstore


@pytest.fixture(scope="module")
def sample_website_document():
    return Document(
        page_content="Zaio offers Fullstack AI Engineer, Data Science, and Cybersecurity Bootcamps with industry mentors.",
        metadata={
            "source_type": "website",
            "source_name": "ZAIO Website",
            "url": "https://www.zaio.io/bootcamps",
            "title": "Zaio Bootcamps",
        },
    )


@pytest.fixture(scope="module")
def prepared_vectorstore(sample_website_document):
    # Module scope builds the vector database once for all retriever tests.
    handbook_docs = load_handbook()
    chunks = split_documents(handbook_docs + [sample_website_document])
    vectorstore = create_vectorstore(chunks)
    return vectorstore

