from pathlib import Path
import pytest


def test_chroma_db_directory_exists():
    chroma_dir = Path("chroma_db")
    assert chroma_dir.exists(), "The Chroma persistence directory should exist"
    assert chroma_dir.is_dir(), "chroma_db should be a directory"


def test_vectorstore_creation_todo():
    pytest.skip(
        "TODO: implement app.services.vectorstore.build_vectorstore and verify returned object and persistence behavior"
    )
