import logging
from typing import List, Optional, Set
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup
from langchain_core.documents import Document

from app.services.text_cleaner import clean_html

logger = logging.getLogger(__name__)

# File extensions and paths to skip when crawling
IGNORED_EXTENSIONS = (
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".pdf", ".css", ".js", ".ico", ".xml", ".json"
)
IGNORED_PATHS = ("/app/login", "/app/signup", "/cdn-cgi/")


def get_page_links(html_content: str, base_url: str) -> List[str]:
    """Extract valid internal links belonging to the same domain from HTML."""
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, "html.parser")
    base_domain = urlparse(base_url).netloc
    found_links: Set[str] = set()

    for anchor in soup.find_all("a", href=True):
        href = anchor.get("href", "").strip()
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue

        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)

        # Ensure link stays on the same domain (e.g. zaio.io or www.zaio.io)
        if parsed.netloc == base_domain or parsed.netloc.endswith(f".{base_domain}"):
            # Filter out ignored extensions and login paths
            if any(parsed.path.lower().endswith(ext) for ext in IGNORED_EXTENSIONS):
                continue
            if any(ignored in parsed.path for ignored in IGNORED_PATHS):
                continue

            # Normalize URL by stripping fragments and query parameters
            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip("/")
            if clean_url:
                found_links.add(clean_url)

    return sorted(list(found_links))


def load_page(url: str, client: Optional[httpx.Client] = None) -> Optional[Document]:
    """Fetch and extract clean text from a single webpage into a LangChain Document."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }

    try:
        if client:
            response = client.get(url, headers=headers, follow_redirects=True, timeout=10.0)
        else:
            response = httpx.get(url, headers=headers, follow_redirects=True, timeout=10.0)

        if response.status_code != 200:
            logger.warning(f"Failed to fetch {url}: status {response.status_code}")
            return None

        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        # Extract page title
        title = soup.title.string.strip() if soup.title and soup.title.string else "ZAIO Page"

        # Clean body text
        cleaned_text = clean_html(html)

        if not cleaned_text:
            return None

        # Return document with structured metadata
        metadata = {
            "source_type": "website",
            "source_name": "ZAIO Website",
            "url": url,
            "title": title,
        }

        return Document(page_content=cleaned_text, metadata=metadata)

    except Exception as error:
        logger.error(f"Error fetching page {url}: {error}")
        return None


def load_website(base_url: str = "https://www.zaio.io", max_pages: int = 15) -> List[Document]:
    """Crawl and extract key pages from the ZAIO website into LangChain Documents."""
    documents: List[Document] = []
    visited_urls: Set[str] = set()
    to_visit: List[str] = [base_url.rstrip("/")]

    with httpx.Client(timeout=10.0) as client:
        while to_visit and len(documents) < max_pages:
            current_url = to_visit.pop(0)

            if current_url in visited_urls:
                continue

            visited_urls.add(current_url)
            doc = load_page(current_url, client=client)

            if doc:
                documents.append(doc)

                # Discover new links from this page if we still have capacity
                if len(documents) < max_pages:
                    try:
                        resp = client.get(current_url, follow_redirects=True)
                        if resp.status_code == 200:
                            new_links = get_page_links(resp.text, base_url)
                            for link in new_links:
                                if link not in visited_urls and link not in to_visit:
                                    to_visit.append(link)
                    except Exception:
                        pass

    return documents
