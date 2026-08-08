from app.database.database import SessionLocal
from app.services.tools import (
    get_all_doctors,
    get_doctor_by_name,
    get_patient_appointments,
)
from app.services.appointment_service import book_appointment


def ai_get_all_doctors():
    """
    Returns all doctors available in the clinic.
    """
    db = SessionLocal()

    try:
        return get_all_doctors(db)
    finally:
        db.close()


def ai_get_doctor_by_name(doctor_name: str):
    """
    Returns information about a doctor.

    Args:
        doctor_name: Full doctor name.
    """
    db = SessionLocal()

    try:
        return get_doctor_by_name(db, doctor_name)
    finally:
        db.close()


def ai_get_patient_appointments(phone: str):
    """
    Returns all appointments for a patient.

    Args:
        phone: Patient phone number.
    """
    db = SessionLocal()

    try:
        return get_patient_appointments(db, phone)
    finally:
        db.close()


def ai_book_appointment(
    patient_name: str,
    phone: str,
    doctor_name: str,
    date: str,
    time: str,
):
    """
    Books an appointment.

    Args:
        patient_name: Patient's full name.
        phone: Patient's phone number.
        doctor_name: Doctor's full name.
        date: Appointment date in YYYY-MM-DD format.
        time: Appointment time in HH:MM format.
    """
    db = SessionLocal()

    try:
        return book_appointment(
            db=db,
            patient_name=patient_name,
            phone=phone,
            doctor_name=doctor_name,
            date=date,
            time=time,
        )
    finally:
        db.close()