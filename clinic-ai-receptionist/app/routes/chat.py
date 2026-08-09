from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.gemini_service import ask_gemini
from app.services.tools import get_all_doctors
from app.services.session_manager import (
    get_session,
    update_session,
)
router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"],
)


class ChatRequest(BaseModel):
    message: str


def generate_ai_reply(
    user_id: str,
    message: str,
    db: Session,
):
    session = get_session(user_id)

    doctors = get_all_doctors(db)

    prompt = f"""
You are an AI Receptionist.

Available doctors:

{doctors}

Conversation Memory:

{session}

Current User Message:

{message}

Instructions:

- Use conversation memory.
- Remember patient name.
- Remember phone number.
- Remember doctor.
- Remember date.
- Remember appointment time.
- Never invent doctors.
- Only use doctors from the database.
"""

    reply = ask_gemini(prompt)

    update_session(
        user_id,
        "last_user_message",
        message,
    )

    update_session(
        user_id,
        "last_ai_reply",
        reply,
    )

    return reply


@router.post("/")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    reply = generate_ai_reply(
        user_id="demo_user",
        message=request.message,
        db=db,
    )

    return {
        "reply": reply
    }