from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.gemini_service import ask_gemini
from app.services.tools import get_all_doctors
from app.services.session_manager import (
    get_session,
    update_session,
    clear_session,
)

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
    # Temporary user ID
    user_id = "demo_user"

    # Load conversation memory
    session = get_session(user_id)

    # Get doctors from database
    doctors = get_all_doctors(db)

    prompt = f"""
You are an AI Receptionist.

Available doctors:

{doctors}

Conversation Memory:

{session}

Current User Message:

{request.message}

Instructions:

- Use the conversation memory whenever relevant.
- Remember previous doctor, date, time and phone if available.
- If the user refers to "tomorrow", "that appointment", "it", etc.,
  use the conversation memory.
- Ask only for missing information.
- Never invent doctors.
- Only use doctors listed above.
- Answer naturally.
"""

    reply = ask_gemini(prompt)

    return {
        "reply": reply
    }