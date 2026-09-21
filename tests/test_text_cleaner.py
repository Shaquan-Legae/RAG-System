from app.services.text_cleaner import clean_html, clean_text


def test_clean_text_normalizes_spaces():
    raw = "Hello   world   this   is   spaced."
    assert clean_text(raw) == "Hello world this is spaced."


def test_clean_text_handles_multiple_newlines():
    raw = "Line 1\n\n\n\n\nLine 2"
    assert clean_text(raw) == "Line 1\n\nLine 2"


def test_clean_text_empty_string():
    assert clean_text("") == ""


def test_clean_html_removes_scripts_and_styles():
    html = """
    <html>
        <head>
            <style>body { color: red; }</style>
            <script>console.log("tracking");</script>
        </head>
        <body>
            <header><nav><a href="/home">Home</a></nav></header>
            <h1>Welcome to ZAIO</h1>
            <p>We provide fullstack AI coding bootcamps.</p>
            <footer><p>Copyright 2026</p></footer>
        </body>
    </html>
    """
    cleaned = clean_html(html)
    assert "console.log" not in cleaned
    assert "body { color: red; }" not in cleaned
    assert "Copyright" not in cleaned
    assert "Home" not in cleaned
    assert "Welcome to ZAIO" in cleaned
    assert "We provide fullstack AI coding bootcamps." in cleaned
