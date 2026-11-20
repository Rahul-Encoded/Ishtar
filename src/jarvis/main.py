from fastapi import FastAPI

from jarvis.api.chat import router as chat_router
from jarvis.api.health import router as health_router

app = FastAPI()

app.include_router(health_router)
app.include_router(chat_router)