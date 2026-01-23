from fastapi import APIRouter
from config.dbConfig import tests, userAnswers
from bson import ObjectId

endpoints = APIRouter()

@endpoints.get("/")
def root():
    return {"message": "Hello from 26-asymmetric!"}

mcqs = [
	{
		"mcqId": ObjectId(),
		"Subject": "Finance",
		"Question": "What is the returns on gold in last 5y?",
		"Answer": "A",
		"Options": [{"A": 212}, {"B": 256}, {"C": 963}, {"D": 654}]
	}
]

userAnswer = [{"mcqId": ObjectId(), "userAnswer": ["B"]}]




@endpoints.post("v1/test")
async def test():
    tests.insert_one(mcqs)
    return {"message": "Test added successfully"}

@endpoints.get("v1/test/{testId}")
async def get_test(testId: ObjectId):
    return tests.find_one({"mcqId": testId})

@endpoints.post("v1/submit-answer")
async def submit_answer():  
    userAnswers.insert_one(userAnswer)
    return {"message": "Answer submitted successfully"}


