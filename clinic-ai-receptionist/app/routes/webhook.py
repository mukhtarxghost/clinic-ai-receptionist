from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse

router = APIRouter()

VERIFY_TOKEN = "clinic_ai_123"


@router.get("/webhook")
async def verify_webhook(
    hub_mode: str,
    hub_verify_token: str,
    hub_challenge: str,
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(hub_challenge)

    return PlainTextResponse("Verification failed", status_code=403)


@router.post("/webhook")
async def receive_message(request: Request):
    body = await request.json()

    print(body)

    return {"status": "received"}