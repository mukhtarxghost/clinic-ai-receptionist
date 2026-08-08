from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.gemini_service import ask_gemini
from app.services.tools import get_all_doctors

router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"]
)


class ChatRequest(BaseModel):
    message: str


@router.post("/")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    doctors = get_all_doctors(db)

    prompt = f"""
You are an AI Receptionist.

Available doctors:

{doctors}

User:
{request.message}

Answer naturally.
Only use the doctor information provided above.
Never invent doctors.
"""

    reply = ask_gemini(prompt)

    return {
        "reply": reply
    }