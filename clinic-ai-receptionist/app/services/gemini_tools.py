from app.database.database import SessionLocal

from app.services.tools import (
    get_all_doctors,
    get_doctor_by_name,
    get_patient_appointments,
)

from app.services.appointment_service import (
    book_appointment,
    cancel_appointment,
    reschedule_appointment,
    get_next_available_slot,
)


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


def ai_cancel_appointment(
    phone: str,
    doctor_name: str = None,
    date: str = None,
):
    """
    Cancels a patient's appointment.

    Args:
        phone: Patient's phone number.
        doctor_name: Doctor's full name (optional).
        date: Appointment date in YYYY-MM-DD format (optional).
    """
    db = SessionLocal()

    try:
        return cancel_appointment(
            db=db,
            phone=phone,
            doctor_name=doctor_name,
            date=date,
        )
    finally:
        db.close()


def ai_reschedule_appointment(
    phone: str,
    doctor_name: str,
    old_date: str,
    old_time: str,
    new_date: str,
    new_time: str,
):
    """
    Reschedules an existing appointment.

    Args:
        phone: Patient phone number.
        doctor_name: Doctor's full name.
        old_date: Current appointment date (YYYY-MM-DD).
        old_time: Current appointment time (HH:MM).
        new_date: New appointment date (YYYY-MM-DD).
        new_time: New appointment time (HH:MM).
    """
    db = SessionLocal()

    try:
        return reschedule_appointment(
            db=db,
            phone=phone,
            doctor_name=doctor_name,
            old_date=old_date,
            old_time=old_time,
            new_date=new_date,
            new_time=new_time,
        )
    finally:
        db.close()


def ai_get_next_available_slot(
    doctor_name: str,
    date: str,
):
    """
    Returns the next available appointment slot for a doctor.

    Args:
        doctor_name: Doctor's full name.
        date: Date in YYYY-MM-DD format.
    """

    print(
        "🔥 NEXT AVAILABLE TOOL CALLED:",
        doctor_name,
        date,
    )

    db = SessionLocal()

    try:
        result = get_next_available_slot(
            db=db,
            doctor_name=doctor_name,
            date=date,
        )

        print(
            "🔥 TOOL RESULT:",
            result,
        )

        return result

    finally:
        db.close()