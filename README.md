# RAG System

A Retrieval-Augmented Generation (RAG) API developed using FastAPI, LangChain, ChromaDB, Sentence Transformers, and Ollama. The application processes a student handbook (PDF), indexes its contents into a vector database, retrieves relevant information for user questions, and generates responses using a locally hosted Llama 3.2 model.

This project is being developed as part of a practical assignment and is designed for future integration with n8n.

---

## Assignment Objectives

The system is required to:

* Load a handbook from a PDF document
* Extract and process the handbook text
* Split the text into manageable chunks
* Generate embeddings for each chunk
* Store embeddings in a Chroma vector database
* Retrieve the most relevant chunks for a user question
* Generate answers using a Large Language Model (LLM)
* Expose the functionality through a FastAPI REST API
* Return JSON responses for future n8n integration

---

## Technologies Used

### Backend

* Python 3.12+
* FastAPI
* Uvicorn

### Retrieval-Augmented Generation

* LangChain
* LangChain Community
* LangChain Text Splitters
* Sentence Transformers
* Ollama
* Llama 3.2

### Vector Database

* ChromaDB

### PDF Processing

* PyPDF

### Utilities

* Pydantic
* Python Dotenv
* HTTPX
* NumPy
* TQDM

### Testing

* Pytest
* Pytest AsyncIO

---

## Project Structure

```text
rag-system/
│
├── app/
│   ├── api/
│   │   └── routes.py
│   │
│   ├── models/
│   │   └── request_models.py
│   │
│   ├── services/
│   │   ├── pdf_loader.py
│   │   ├── text_splitter.py
│   │   ├── embeddings.py
│   │   ├── vectorstore.py
│   │   ├── retriever.py
│   │   ├── llm.py
│   │   └── rag.py
│   │
│   ├── config.py
│   └── main.py
│
├── chroma_db/
├── handbook/
│   └── handbook.pdf
├── tests/
├── .env
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd rag-system
```

### 2. Create a Virtual Environment

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**

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

Create a `.env` file in the project root.

```env
OLLAMA_MODEL=llama3.2
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

Place the handbook PDF inside the `handbook` directory.

```text
handbook/
└── handbook.pdf
```

---

## Running Ollama

Download the model if required.

```bash
ollama pull llama3.2
```

Start the Ollama server.

```bash
ollama serve
```

---

## Running the Application

Start the FastAPI development server.

```bash
uvicorn app.main:app --reload
```

Once running, the application will be available at:

| URL                         | Description |
| --------------------------- | ----------- |
| http://127.0.0.1:8000       | API         |
| http://127.0.0.1:8000/docs  | Swagger UI  |
| http://127.0.0.1:8000/redoc | ReDoc       |

---

## API Endpoints

| Method | Endpoint  | Description                              |
| ------ | --------- | ---------------------------------------- |
| GET    | `/`       | Returns the API status                   |
| GET    | `/health` | Health check                             |
| GET    | `/chunks` | Returns the number of indexed chunks     |
| POST   | `/reload` | Reloads and rebuilds the vector database |
| POST   | `/ask`    | Answers questions using the handbook     |

---

## Example Request

```http
POST /ask
Content-Type: application/json
```

```json
{
    "question": "What is the attendance requirement?"
}
```

---

## Example Response

```json
{
    "answer": "Students are required to attend the minimum number of classes specified in the handbook.",
    "source": "Page 12"
}
```

---

## RAG Workflow

```text
                     handbook.pdf
                           │
                           ▼
                    Load PDF Document
                           │
                           ▼
                   Extract Handbook Text
                           │
                           ▼
                  Split Text into Chunks
                           │
                           ▼
          Generate Embeddings (MiniLM)
                           │
                           ▼
              Store Embeddings in ChromaDB
                           │
                           ▲
                           │
                  Receive User Question
                           │
                           ▼
            Generate Question Embedding
                           │
                           ▼
          Retrieve Relevant Document Chunks
                           │
                           ▼
          Build Prompt with Retrieved Context
                           │
                           ▼
            Llama 3.2 via Ollama Generates Answer
                           │
                           ▼
              Return JSON Response from FastAPI
```

---

## Testing

Run the test suite.

```bash
pytest
```

Run tests with verbose output.

```bash
pytest -v
```

You can also test the API using:

* Swagger UI
* Thunder Client
* Postman

---

## Future n8n Integration

The API is designed so that the `POST /ask` endpoint can be consumed directly by an n8n HTTP Request node.

Example payload:

```json
{
    "question": "{{$json.message}}"
}
```

The response can then be used in automation workflows for messaging platforms, notifications, or other integrations.

