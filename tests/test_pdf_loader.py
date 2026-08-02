from pathlib import Path
import pytest


def test_handbook_pdf_exists():
    handbook_path = Path("handbook") / "handbook.pdf"
    assert handbook_path.exists(), "handbook.pdf should exist in the handbook folder"


def test_load_pdf_todo():
    pytest.skip("TODO: implement app.services.pdf_loader.load_pdf and test PDF loading behavior")


def test_pdf_documents_todo():
    pytest.skip(
        "TODO: once load_pdf is implemented, verify the document list is not empty and each document contains text"
    )
