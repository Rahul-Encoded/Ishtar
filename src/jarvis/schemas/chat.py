from datetime import datetime
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(min_length=1)

class ChatResponse(BaseModel):
    message: str
    timestamp: datetime