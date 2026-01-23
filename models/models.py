from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import uuid4
from typing import Optional, List

class User(BaseModel):
    name:str
    email: EmailStr
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Mcq(BaseModel):
    subject: str
    question: str
    options: List[dict[str, str]]
    answer: str

class Test(BaseModel):
    mcqs: List[Mcq]
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: datetime = Field(default_factory=datetime.utcnow)

class TestScore(BaseModel):
    userId: str
    mcqId: str
    userAnswer: List[str]
    totalScore: int
    SubjectWiseScore: dict[str, int]
    totalTimeTaken: int