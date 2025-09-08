from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from qdrant_client import QdrantClient

import config
from src.retrieval import retrieve_documents
from src.generate import generate_answer


app = FastAPI(title="Middle Earth Saga", version="1.0")


client = QdrantClient(
    url=config.QDRANT_URL,
    api_key=config.QDRANT_API_KEY,
    timeout=120.0  # increase timeout for large inserts
)

class GenerationRequest(BaseModel):
    query: str
    top_k: int = 5
    model_name: str = "gpt-4o-mini"
    temperature: float = 0.0

class GenerationResponse(BaseModel):
    answer: str


@app.get("/")
def health_check():
    return {"status_code": 200, "message": "OK"}


@app.post("/chat")
async def generate_text(request: GenerationRequest):
    try:
        # Step 2: Retrieve documents
        retrieved_docs = retrieve_documents(
            client=client,
            query=request.query,
            collection_name=config.COLLECTION_NAME,
            k=request.top_k
        )

        if not retrieved_docs:
            raise HTTPException(status_code=404, detail="No documents retrieved for query")
        
        answer = generate_answer(query=request.query, retrieved_docs=retrieved_docs)

        return GenerationResponse(
            answer=answer
        )
    except Exception as e:
        print(f"Request failed due to {e}")