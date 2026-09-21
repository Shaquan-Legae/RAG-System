from typing import Optional
from langchain_core.documents import Document


def format_source(document: Optional[Document]) -> str:
    """Format document metadata into a human-readable source reference string."""
    if not document or not hasattr(document, "metadata") or not document.metadata:
        return "Unknown"

    metadata = document.metadata
    source_type = metadata.get("source_type")

    if source_type == "website" or "url" in metadata:
        url = metadata.get("url", "https://www.zaio.io")
        return url

    if source_type == "handbook" or "page" in metadata:
        page = metadata.get("page")
        if page is not None:
            return f"Student Handbook - Page {page}"
        return "Student Handbook"

    # Generic fallback based on source_name if available
    source_name = metadata.get("source_name", "Knowledge Base")
    return source_name
