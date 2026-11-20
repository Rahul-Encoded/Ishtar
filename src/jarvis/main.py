from fastapi import FastAPI
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime

class ChatRequest(BaseModel):
    message: str = Field(min_length=1)

class ChatResponse(BaseModel):
    message: str
    timestamp: datetime


app = FastAPI()

@app.get("/health")
def get_health() -> HealthResponse:
    return HealthResponse(
        status = "ok",
        version = "1.0.0",
        timestamp = datetime.now(timezone.utc)
    )

@app.post("/chat", response_model=ChatResponse)
def post_chat(request: ChatRequest) -> ChatResponse:
    return ChatResponse(
        message = f"Ishtar recieved your message: {request.message}",
        timestamp=datetime.now(timezone.utc),
    )