from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.routes.chat import generate_ai_reply
from app.services.whatsapp_service import send_whatsapp_message

router = APIRouter()

VERIFY_TOKEN = "clinic_ai_123"


@router.get("/webhook")
async def verify_webhook(
    hub_mode: str,
    hub_verify_token: str,
    hub_challenge: str,
):
    if (
        hub_mode == "subscribe"
        and hub_verify_token == VERIFY_TOKEN
    ):
        return PlainTextResponse(hub_challenge)

    return PlainTextResponse(
        "Verification failed",
        status_code=403,
    )


@router.post("/webhook")
async def receive_message(request: Request):
    body = await request.json()

    print("=" * 80)
    print("Incoming WhatsApp Webhook")
    print(body)
    print("=" * 80)

    try:
        entry = body["entry"][0]
        change = entry["changes"][0]
        value = change["value"]

        # Ignore delivery/read/status updates
        if "messages" not in value:
            print("Ignoring status update...")
            return {"status": "ignored"}

        message = value["messages"][0]

        # Ignore non-text messages
        if message["type"] != "text":
            print("Unsupported message type:", message["type"])
            return {"status": "unsupported"}

        phone = message["from"]
        user_message = message["text"]["body"]

        print(f"Phone: {phone}")
        print(f"Message: {user_message}")

        db: Session = SessionLocal()

        try:
            ai_reply = generate_ai_reply(
                user_id=phone,
                message=user_message,
                db=db,
            )
        finally:
            db.close()

        print("Gemini Reply:")
        print(ai_reply)

        response = send_whatsapp_message(
            phone=phone,
            message=ai_reply,
        )

        print("WhatsApp API Response:")
        print(response)

        return {"status": "success"}

    except Exception as e:
        print("Webhook Error")
        print(str(e))
        return {
            "status": "error",
            "message": str(e),
        }