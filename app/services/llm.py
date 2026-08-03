import ollama

from app.config import OLLAMA_MODEL


def generate_response(prompt: str) -> str:
    """Send a prompt to Ollama and return the generated response text."""

    response = ollama.generate(model=OLLAMA_MODEL, prompt=prompt)
    text = response.response or ""

    return text
