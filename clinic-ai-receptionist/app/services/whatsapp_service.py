import os
import requests
from dotenv import load_dotenv

load_dotenv()

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

if not WHATSAPP_TOKEN:
    raise ValueError("WHATSAPP_TOKEN is missing")

if not PHONE_NUMBER_ID:
    raise ValueError("PHONE_NUMBER_ID is missing")

GRAPH_URL = f"https://graph.facebook.com/v23.0/{PHONE_NUMBER_ID}/messages"


def send_whatsapp_message(phone: str, message: str):
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {
            "body": message
        },
    }

    response = requests.post(
        GRAPH_URL,
        headers=headers,
        json=payload,
        timeout=30,
    )

    print("WhatsApp Status:", response.status_code)
    print("WhatsApp Response:", response.text)

    response.raise_for_status()

    try:
        return response.json()
    except Exception:
        return {
            "status_code": response.status_code,
            "response": response.text,
        }