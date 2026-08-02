from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="RAG API")

app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "RAG API root"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
