import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.services.gemini_tools import (
    ai_get_all_doctors,
    ai_get_doctor_by_name,
    ai_get_patient_appointments,
    ai_book_appointment,
)

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_gemini(prompt: str):

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction="""
You are an AI Receptionist for a medical clinic.

You have access to backend tools.

Responsibilities:
- Help patients find doctors.
- Help patients book appointments.
- Help patients cancel appointments.
- Help patients check available slots.
- Answer politely and professionally.

Rules:

- Whenever the user asks to book or schedule an appointment, use the booking tool.
- Whenever the user asks about doctors, use the appropriate doctor tool.
- Whenever the user asks about their appointments, use the patient appointments tool.
- If any required booking information is missing (patient name, phone number, doctor name, date, or time), ask ONLY for the missing information before using the booking tool.
- Never invent doctors.
- Never invent appointments.
- Never invent working hours.
- Never invent appointment confirmations.
- Always use the available backend tools whenever clinic information or actions are required.
- If information is unavailable, politely say so.
""",
            tools=[
                ai_get_all_doctors,
                ai_get_doctor_by_name,
                ai_get_patient_appointments,
                ai_book_appointment,
            ],
        ),
    )

    return response.text