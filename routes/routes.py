from fastapi import APIRouter

endpoints = APIRouter()

@endpoints.get("/")
def root():
    return {"message": "Hello from 26-asymmetric!"}

