from datetime import datetime, timezone
from fastapi import APIRouter
from jarvis.schemas.health import HealthResponse

router = APIRouter()

@router.get("/health")
def get_health() -> HealthResponse:
    return HealthResponse(
        status = "ok",
        version = "1.0.0",
        timestamp = datetime.now(timezone.utc)
    )