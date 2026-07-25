from fastapi import APIRouter
from pydantic import BaseModel

from services.chatbot import chatbot

router = APIRouter(
    prefix="/chat",
    tags=["Recruiter Chat"]
)

class ChatRequest(BaseModel):
    context: str
    question: str


@router.post("/")
def ask(request: ChatRequest):

    answer = chatbot.answer(
        request.context,
        request.question
    )

    return {
        "answer": answer
    }