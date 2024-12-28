from fastapi import APIRouter
from app.services.rag_agent import query_documents

router = APIRouter()

@router.get("/ask")
def ask_question(query: str):
    return query_documents(query)
