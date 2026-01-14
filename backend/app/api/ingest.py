from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
from app.worker import process_chat_log

router = APIRouter()

class MessagePayload(BaseModel):
    role: str
    content: str

class ChatLogPayload(BaseModel):
    provider: str
    thread_id: Optional[str] = None
    messages: List[MessagePayload]
    api_key: str # For now, simple auth via payload

@router.post("/ingest")
async def ingest_chat(payload: ChatLogPayload):
    # Push to Celery
    task = process_chat_log.delay(payload.dict())
    return {"status": "accepted", "task_id": str(task.id)}

@router.get("/context")
async def get_context(query: str):
    # Placeholder for vector search
    # In real implementation, this would query pgvector
    return {
        "context": [
            "User prefers Python over Java.",
            "User is building a memory sync tool."
        ]
    }
