from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/health")
def get_health() -> dict[str, str]:
    api_status: dict[str, str] = {
        "status": "ok",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }
    
    return api_status

