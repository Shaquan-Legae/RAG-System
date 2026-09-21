from unittest.mock import MagicMock, patch

from langchain_core.documents import Document

from app.services.website_loader import get_page_links, load_page, load_website


def test_get_page_links_filters_external_and_media():
    html = """
    <html>
        <body>
            <a href="/courses">Courses</a>
            <a href="https://www.zaio.io/aboutus">About</a>
            <a href="https://google.com/external">External</a>
            <a href="/image.png">Image</a>
            <a href="/app/login">Login</a>
        </body>
    </html>
    """
    links = get_page_links(html, base_url="https://www.zaio.io")
    assert "https://www.zaio.io/courses" in links
    assert "https://www.zaio.io/aboutus" in links
    assert not any("google.com" in link for link in links)
    assert not any(link.endswith(".png") for link in links)
    assert not any("/app/login" in link for link in links)


@patch("httpx.get")
def test_load_page_success(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.text = """
    <html>
        <head><title>Fullstack Course</title></head>
        <body>
            <h1>Fullstack Course</h1>
            <p>Learn Python and FastAPI.</p>
        </body>
    </html>
    """
    mock_get.return_value = mock_resp

    doc = load_page("https://www.zaio.io/fullstack")
    assert doc is not None
    assert isinstance(doc, Document)
    assert "Fullstack Course" in doc.page_content
    assert doc.metadata["url"] == "https://www.zaio.io/fullstack"
    assert doc.metadata["source_type"] == "website"
    assert doc.metadata["source_name"] == "ZAIO Website"



@patch("app.services.website_loader.load_page")
def test_load_website_respects_max_pages(mock_load_page):
    mock_load_page.return_value = Document(
        page_content="Mock page",
        metadata={"source_type": "website", "url": "https://www.zaio.io"},
    )
    docs = load_website(base_url="https://www.zaio.io", max_pages=2)
    assert len(docs) <= 2
