import re
from bs4 import BeautifulSoup


def clean_text(text: str) -> str:
    """Normalize whitespace and remove excessive blank lines from text."""
    if not text:
        return ""

    # Replace multiple spaces with a single space
    text = re.sub(r"[ \t]+", " ", text)
    # Replace multiple newlines with double newlines
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    # Strip leading/trailing whitespace
    return text.strip()


def clean_html(html_content: str) -> str:
    """Extract clean readable text from HTML content, discarding boilerplate."""
    if not html_content:
        return ""

    soup = BeautifulSoup(html_content, "html.parser")

    # Remove script, style, navigation, footer, and header elements
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "svg"]):
        tag.decompose()

    # Get extracted text separated by newlines
    text = soup.get_text(separator="\n")

    return clean_text(text)
