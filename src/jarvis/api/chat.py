from fastapi import APIRouter
from jarvis.schemas.chat import ChatRequest, ChatResponse
from datetime import datetime, timezone

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def post_chat(request: ChatRequest) -> ChatResponse:
    return ChatResponse(
        message = f"Ishtar recieved your message: {request.message}",
        timestamp=datetime.now(timezone.utc),
    )