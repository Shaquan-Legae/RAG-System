# Multi-Source RAG System (AI Capstone Project)

A Retrieval-Augmented Generation (RAG) API developed using **FastAPI**, **LangChain**, **ChromaDB**, **Sentence Transformers (MiniLM)**, and **Ollama (Llama 3.2)**. 

The system provides intelligent question answering grounded in two knowledge sources:
1. 📄 **Student Handbook (PDF)**
2. 🌐 **ZAIO Official Website** ([https://www.zaio.io](https://www.zaio.io))

The system indexes both knowledge sources into a unified Chroma vector database, performs similarity retrieval with score thresholding, generates accurate responses using context only, attributes answers to their exact source, and strictly refuses unsupported questions.

---

## Architecture & Workflow

```text
  📄 Student Handbook (PDF)              🌐 ZAIO Website (https://www.zaio.io)
             │                                              │
             ▼                                              ▼
   PyPDF Text Extractor                           HTTP Web Crawler & Parser
             │                                              │
             ▼                                              ▼
  Handbook Normalization                        HTML Sanitizer & Text Cleaner
             │                                              │
             └──────────────────────┬───────────────────────┘
                                    │
                                    ▼
                      Recursive Text Splitter (500 / 100)
                                    │
                                    ▼
                    Source Metadata Tagging (Page / URL)
                                    │
                                    ▼
                  Sentence Transformer Embeddings (MiniLM)
                                    │
                                    ▼
                      Unified Chroma Vector Database
                                    │
   ─────────────────────────────────┼─────────────────────────────────
   Query Execution & Retrieval Flow │
                                    ▼
                       User Question (POST /ask)
                                    │
                                    ▼
                       Question Vector Embedding
                                    │
                                    ▼
                  Similarity Search with Score Threshold
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
       Relevant Chunks Found             No Match (Above Threshold)
                    │                               │
                    ▼                               ▼
      Context-Grounded Prompt          Exact Fallback Response:
                    │                  "I could not find that information
                    ▼                   in the available knowledge base."
       Ollama (Llama 3.2 Model)                     │
                    │                               │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                     Answer + Formatted Source Citation
```

---

## Key Features

- **Dual-Source Ingestion**: Ingests both local PDF documents (`handbook/handbook.pdf`) and live web pages from `https://www.zaio.io` (courses, bootcamps, about pages).
- **Text Sanitization**: Strips scripts, navigation headers, footers, and redundant whitespace.
- **Unified Vector Storage**: Embeds and stores chunks from both sources in a single persistent ChromaDB collection.
- **Source Attribution**: Retains exact metadata to cite either `"Student Handbook - Page X"` or `"https://www.zaio.io/..."`.
- **Similarity Score Thresholding**: Prevents hallucinations by rejecting out-of-domain questions before LLM inference.
- **Standardized Fallback**: Strictly responds with `"I could not find that information in the available knowledge base."` when no relevant context exists.
- **Microservice Separation**: Clean separation of concerns between API endpoints, Ingestion, Vector Storage, Retriever, Answer Generator, and Utilities.
- **n8n Automation Ready**: Includes an exported n8n workflow for conversational integration.

---

## Project Structure

```text
rag-system/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py              # FastAPI endpoints (/, /health, /chunks, /reload, /ask)
│   ├── models/
│   │   ├── __init__.py
│   │   └── request_models.py      # Pydantic schemas (QuestionRequest, QuestionResponse)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── embeddings.py          # HuggingFace sentence-transformers loader
│   │   ├── llm.py                 # Ollama text generation client
│   │   ├── pdf_loader.py          # PyPDF loader with text normalization & metadata
│   │   ├── rag.py                 # RAG orchestrator with strict prompt & fallback
│   │   ├── retriever.py           # Similarity search with score threshold filtering
│   │   ├── text_cleaner.py        # Whitespace and HTML boilerplate cleaner
│   │   ├── text_splitter.py       # Recursive text chunking
│   │   ├── vectorstore.py         # Chroma vector store persistence management
│   │   └── website_loader.py      # ZAIO website crawler and parser
│   ├── utils/
│   │   ├── __init__.py
│   │   └── source_formatter.py    # Formats citations (Page number or URL)
│   ├── config.py                  # Environment settings & thresholds
│   └── main.py                    # Application entry point
├── handbook/
│   └── handbook.pdf               # Active student handbook
├── n8n/
│   └── rag_workflow.json          # Ready-to-import n8n workflow
├── tests/
│   ├── conftest.py                # Shared test fixtures (dual-source Chroma setup)
│   ├── test_api.py                # API endpoint tests
│   ├── test_embeddings.py         # Embedding model tests
│   ├── test_llm.py                # Ollama client tests
│   ├── test_pdf_loader.py         # PDF loader tests
│   ├── test_rag.py                # Dual-source RAG pipeline tests
│   ├── test_retriever.py          # Retriever & threshold tests
│   ├── test_source_formatter.py   # Citation formatting tests
│   ├── test_text_cleaner.py       # Text cleaning tests
│   ├── test_text_splitter.py      # Text splitter tests
│   ├── test_vectorstore.py        # Vector database persistence tests
│   └── test_website_loader.py     # Website crawler & parser tests
├── chroma_db/                     # Persistent ChromaDB storage directory
├── .env                           # Environment variables
├── requirements.txt               # Project dependencies
└── README.md                      # Documentation
```

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd rag-system
```

### 2. Create and Activate a Virtual Environment

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create or update `.env` in the project root:

```env
OLLAMA_MODEL=llama3.2
EMBEDDING_MODEL=all-MiniLM-L6-v2
ZAIO_URL=https://www.zaio.io
SCORE_THRESHOLD=1.45
```

---

## Running Ollama (LLM)

1. Download the Llama 3.2 model:
   ```bash
   ollama pull llama3.2
   ```
2. Start the Ollama local server:
   ```bash
   ollama serve
   ```

---

## Running the API Server

Start the FastAPI development server:
```bash
uvicorn app.main:app --reload
```

Interactive API documentation will be available at:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | API status check |
| `GET` | `/health` | Application health check |
| `GET` | `/chunks` | Total indexed chunks count across both sources |
| `POST` | `/reload` | Reloads Handbook & ZAIO Website and rebuilds ChromaDB |
| `POST` | `/ask` | Queries the dual-source RAG system |

---

## Example API Queries

### 1. Student Handbook Query
**Request:**
```http
POST /ask
Content-Type: application/json

{
  "question": "What is the attendance requirement?"
}
```

**Response:**
```json
{
  "answer": "Students are required to maintain active attendance and attend live sessions scheduled between 6 pm - 8 pm on Thursdays.",
  "source": "Student Handbook - Page 10"
}
```

---

### 2. ZAIO Website Query
**Request:**
```http
POST /ask
Content-Type: application/json

{
  "question": "What courses does ZAIO offer?"
}
```

**Response:**
```json
{
  "answer": "Zaio offers bootcamps in Fullstack AI Engineering, Data Science, Cybersecurity, and Digital Marketing with mentor-led training.",
  "source": "https://www.zaio.io"
}
```

---

### 3. Out-of-Domain / Unsupported Query
**Request:**
```http
POST /ask
Content-Type: application/json

{
  "question": "What is the population of Japan?"
}
```

**Response:**
```json
{
  "answer": "I could not find that information in the available knowledge base.",
  "source": null
}
```

---

## Automated Testing

Run the complete test suite:
```bash
PYTHONPATH=. pytest
```

Run with detailed verbose output:
```bash
PYTHONPATH=. pytest -v
```

### Test Coverage Summary
- `test_api.py`: Validates `/`, `/health`, `/chunks`, `/reload`, and `/ask` response schemas.
- `test_website_loader.py`: Validates domain-bounded URL crawling and HTML content extraction.
- `test_text_cleaner.py`: Validates removal of boilerplate tags (`<script>`, `<nav>`, `<footer>`) and whitespace normalization.
- `test_source_formatter.py`: Validates citation generation for both handbook pages and website URLs.
- `test_retriever.py`: Validates cross-source similarity search and score threshold rejection.
- `test_rag.py`: Validates context grounding, source propagation, and strict fallback strings.
- `test_pdf_loader.py`: Validates PDF loading and metadata attachment.
- `test_embeddings.py`: Validates sentence-transformer embedding model.
- `test_vectorstore.py`: Validates ChromaDB persistence and querying.

---

## n8n Integration

The system includes a pre-built workflow configuration in [`n8n/rag_workflow.json`](n8n/rag_workflow.json).

### Setup in n8n:
1. Open n8n (`http://localhost:5678`).
2. Select **Workflows > Import from File** and select `n8n/rag_workflow.json`.
3. The workflow receives incoming questions via **Webhook Trigger**, sends a request to `http://localhost:8000/ask`, formats the response (Answer + Source Citation), and returns the JSON payload.

---

## Limitations

- **Website Crawling Scope**: Crawling is strictly bounded to internal pages within `https://www.zaio.io` to ensure fast indexing and prevent external scraping.
- **Offline Mode**: If Ollama is not running locally, unit tests gracefully skip LLM inference while testing all ingestion, vector search, and API routing logic.
