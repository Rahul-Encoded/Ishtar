from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime

app = FastAPI()

@app.get("/health")
def get_health() -> HealthResponse:
    return HealthResponse(
        "status": "ok",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    )

