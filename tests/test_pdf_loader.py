from app.config import HANDBOOK_PATH
from app.services.pdf_loader import load_handbook


def test_handbook_pdf_exists():
    assert HANDBOOK_PATH.exists(), f"Handbook not found: {HANDBOOK_PATH}"


def test_load_handbook_returns_list():
    documents = load_handbook()
    assert isinstance(documents, list)


def test_load_handbook_list_not_empty():
    documents = load_handbook()
    assert len(documents) > 0


def test_first_document_contains_text():
    documents = load_handbook()
    assert documents[0].page_content.strip()
