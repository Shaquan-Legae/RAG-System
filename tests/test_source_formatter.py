from langchain_core.documents import Document

from app.utils.source_formatter import format_source


def test_format_source_website():
    doc = Document(
        page_content="Course content",
        metadata={
            "source_type": "website",
            "source_name": "ZAIO Website",
            "url": "https://www.zaio.io/courses",
        },
    )
    assert format_source(doc) == "https://www.zaio.io/courses"


def test_format_source_handbook():
    doc = Document(
        page_content="Handbook content",
        metadata={
            "source_type": "handbook",
            "source_name": "Student Handbook",
            "page": 18,
        },
    )
    assert format_source(doc) == "Student Handbook - Page 18"


def test_format_source_none_or_empty():
    assert format_source(None) == "Unknown"
    doc_no_meta = Document(page_content="No metadata")
    assert format_source(doc_no_meta) == "Unknown"

