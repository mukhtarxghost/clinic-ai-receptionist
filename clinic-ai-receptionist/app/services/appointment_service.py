from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.doctor_leave import DoctorLeave


# ---------------------------------------------------------
# DATE HELPERS
# ---------------------------------------------------------

def normalize_date(value):
    """
    Convert supported date formats into YYYY-MM-DD.

    Supported:
    - YYYY-MM-DD
    - DD/MM/YYYY
    - DD-MM-YYYY
    - YYYY/MM/DD
    """

    if value is None:
        return None

    value = str(value).strip()

    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y/%m/%d",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue

    return None


def normalize_time(value):
    """
    Convert supported time formats into HH:MM.
    """

    if value is None:
        return None

    value = str(value).strip()

    formats = [
        "%H:%M",
        "%H:%M:%S",
        "%I:%M %p",
        "%I:%M%p",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt).strftime("%H:%M")
        except ValueError:
            continue

    return None


# ---------------------------------------------------------
# DOCTOR LEAVE CHECK
# ---------------------------------------------------------

def doctor_is_on_leave(
    db: Session,
    doctor_id: int,
    requested_date: str,
):
    """
    Check whether a doctor is on leave on a requested date.
    """

    requested = normalize_date(requested_date)

    if requested is None:
        return False

    leaves = db.query(DoctorLeave).filter(
        DoctorLeave.doctor_id == doctor_id
    ).all()

    for leave in leaves:
        leave_date = normalize_date(leave.date)

        if leave_date == requested:
            return True

    return False


# ---------------------------------------------------------
# TIME VALIDATION
# ---------------------------------------------------------

def is_valid_time(
    doctor,
    requested_time: str,
):
    """
    Check whether requested appointment time falls
    inside the doctor's working hours.
    """

    requested = normalize_time(requested_time)

    if requested is None:
        return False

    start = normalize_time(doctor.start_time)
    end = normalize_time(doctor.end_time)

    if start is None or end is None:
        return False

    requested_dt = datetime.strptime(
        requested,
        "%H:%M"
    )

    start_dt = datetime.strptime(
        start,
        "%H:%M"
    )

    end_dt = datetime.strptime(
        end,
        "%H:%M"
    )

    return start_dt <= requested_dt < end_dt


# ---------------------------------------------------------
# BOOK APPOINTMENT
# ---------------------------------------------------------

def book_appointment(
    db: Session,
    patient_name: str,
    phone: str,
    doctor_name: str,
    date: str,
    time: str,
):
    requested_date = normalize_date(date)
    requested_time = normalize_time(time)

    if requested_date is None:
        return {
            "success": False,
            "message": "Invalid appointment date. Please use YYYY-MM-DD."
        }

    if requested_time is None:
        return {
            "success": False,
            "message": "Invalid appointment time. Please use HH:MM."
        }

    doctor = db.query(Doctor).filter(
        Doctor.name == doctor_name
    ).first()

    if doctor is None:
        return {
            "success": False,
            "message": "Doctor not found."
        }

    # -----------------------------------------------------
    # LEAVE CHECK
    # -----------------------------------------------------

    if doctor_is_on_leave(
        db,
        doctor.id,
        requested_date,
    ):
        return {
            "success": False,
            "message": (
                f"{doctor.name} is on leave on "
                f"{requested_date}."
            )
        }

    # -----------------------------------------------------
    # WORKING HOURS CHECK
    # -----------------------------------------------------

    if not is_valid_time(
        doctor,
        requested_time,
    ):
        return {
            "success": False,
            "message": (
                f"{doctor.name} is not available at "
                f"{requested_time}. "
                f"Working hours are "
                f"{doctor.start_time} to {doctor.end_time}."
            )
        }

    # -----------------------------------------------------
    # SLOT CHECK
    # -----------------------------------------------------

    existing = db.query(Appointment).filter(
        Appointment.doctor == doctor_name,
        Appointment.date == requested_date,
        Appointment.time == requested_time,
    ).first()

    if existing:
        return {
            "success": False,
            "message": "Slot already booked."
        }

    # -----------------------------------------------------
    # CREATE APPOINTMENT
    # -----------------------------------------------------

    appointment = Appointment(
        patient_name=patient_name,
        phone=phone,
        doctor=doctor_name,
        date=requested_date,
        time=requested_time,
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return {
        "success": True,
        "appointment": "Appointment created successfully",
        "appointment_id": appointment.id,
        "doctor": doctor_name,
        "date": requested_date,
        "time": requested_time,
    }


# ---------------------------------------------------------
# CANCEL APPOINTMENT
# ---------------------------------------------------------

def cancel_appointment(
    db: Session,
    phone: str,
    doctor_name: str = None,
    date: str = None,
):
    query = db.query(Appointment).filter(
        Appointment.phone == phone
    )

    if doctor_name:
        query = query.filter(
            Appointment.doctor == doctor_name
        )

    if date:
        requested_date = normalize_date(date)

        if requested_date is None:
            return {
                "success": False,
                "message": "Invalid appointment date."
            }

        query = query.filter(
            Appointment.date == requested_date
        )

    appointment = query.first()

    if appointment is None:
        return {
            "success": False,
            "message": "No matching appointment found."
        }

    db.delete(appointment)
    db.commit()

    return {
        "success": True,
        "message": "Appointment cancelled successfully."
    }


# ---------------------------------------------------------
# RESCHEDULE APPOINTMENT
# ---------------------------------------------------------

def reschedule_appointment(
    db: Session,
    phone: str,
    doctor_name: str,
    old_date: str,
    old_time: str,
    new_date: str,
    new_time: str,
):
    old_date = normalize_date(old_date)
    old_time = normalize_time(old_time)
    new_date = normalize_date(new_date)
    new_time = normalize_time(new_time)

    if not old_date or not new_date:
        return {
            "success": False,
            "message": "Invalid appointment date."
        }

    if not old_time or not new_time:
        return {
            "success": False,
            "message": "Invalid appointment time."
        }

    appointment = db.query(Appointment).filter(
        Appointment.phone == phone,
        Appointment.doctor == doctor_name,
        Appointment.date == old_date,
        Appointment.time == old_time,
    ).first()

    if appointment is None:
        return {
            "success": False,
            "message": "Appointment not found."
        }

    doctor = db.query(Doctor).filter(
        Doctor.name == doctor_name
    ).first()

    if doctor is None:
        return {
            "success": False,
            "message": "Doctor not found."
        }

    # -----------------------------------------------------
    # LEAVE CHECK
    # -----------------------------------------------------

    if doctor_is_on_leave(
        db,
        doctor.id,
        new_date,
    ):
        return {
            "success": False,
            "message": (
                f"{doctor.name} is on leave on "
                f"{new_date}."
            )
        }

    # -----------------------------------------------------
    # WORKING HOURS CHECK
    # -----------------------------------------------------

    if not is_valid_time(
        doctor,
        new_time,
    ):
        return {
            "success": False,
            "message": (
                f"{doctor.name} is not available at "
                f"{new_time}. "
                f"Working hours are "
                f"{doctor.start_time} to {doctor.end_time}."
            )
        }

    # -----------------------------------------------------
    # SLOT CHECK
    # -----------------------------------------------------

    existing = db.query(Appointment).filter(
        Appointment.doctor == doctor_name,
        Appointment.date == new_date,
        Appointment.time == new_time,
        Appointment.id != appointment.id,
    ).first()

    if existing:
        return {
            "success": False,
            "message": "Requested slot is already booked."
        }

    # -----------------------------------------------------
    # UPDATE
    # -----------------------------------------------------

    appointment.date = new_date
    appointment.time = new_time

    db.commit()
    db.refresh(appointment)

    return {
        "success": True,
        "message": "Appointment rescheduled successfully.",
        "date": new_date,
        "time": new_time,
    }


# ---------------------------------------------------------
# NEXT AVAILABLE SLOT
# ---------------------------------------------------------

def get_next_available_slot(
    db: Session,
    doctor_name: str,
    date: str,
):
    requested_date = normalize_date(date)

    if requested_date is None:
        return {
            "success": False,
            "message": "Invalid date. Please use YYYY-MM-DD."
        }

    doctor = db.query(Doctor).filter(
        Doctor.name == doctor_name
    ).first()

    if doctor is None:
        return {
            "success": False,
            "message": "Doctor not found."
        }

    # -----------------------------------------------------
    # LEAVE CHECK
    # -----------------------------------------------------

    if doctor_is_on_leave(
        db,
        doctor.id,
        requested_date,
    ):
        return {
            "success": False,
            "message": (
                f"{doctor.name} is on leave on "
                f"{requested_date}."
            )
        }

    # -----------------------------------------------------
    # EXISTING BOOKINGS
    # -----------------------------------------------------

    booked = db.query(Appointment).filter(
        Appointment.doctor == doctor_name,
        Appointment.date == requested_date,
    ).all()

    # -----------------------------------------------------
    # DEBUG
    # -----------------------------------------------------

    print("🔥 DEBUG DOCTOR:", doctor.name)
    print("🔥 DEBUG DATE:", requested_date)
    print("🔥 DEBUG START:", doctor.start_time)
    print("🔥 DEBUG END:", doctor.end_time)
    print("🔥 DEBUG DURATION:", doctor.appointment_duration)

    print("🔥 DEBUG BOOKINGS:", [
        {
            "id": a.id,
            "doctor": a.doctor,
            "date": a.date,
            "time": a.time,
        }
        for a in booked
    ])

    # -----------------------------------------------------
    # NORMALIZE BOOKED SLOTS
    # -----------------------------------------------------

    booked_slots = {
        normalize_time(appointment.time)
        for appointment in booked
    }

    print("🔥 DEBUG BOOKED SLOTS:", booked_slots)

    # -----------------------------------------------------
    # GENERATE SLOTS
    # -----------------------------------------------------

    start = normalize_time(doctor.start_time)
    end = normalize_time(doctor.end_time)

    if start is None or end is None:
        return {
            "success": False,
            "message": "Doctor working hours are invalid."
        }

    print("🔥 DEBUG NORMALIZED START:", start)
    print("🔥 DEBUG NORMALIZED END:", end)

    current = datetime.strptime(
        start,
        "%H:%M"
    )

    end_dt = datetime.strptime(
        end,
        "%H:%M"
    )

    while current < end_dt:

        slot = current.strftime("%H:%M")

        print(
            "🔥 DEBUG CHECKING SLOT:",
            slot,
            "| BOOKED:",
            slot in booked_slots
        )

        if slot not in booked_slots:
            print("🔥 DEBUG FREE SLOT FOUND:", slot)

            return {
                "success": True,
                "date": requested_date,
                "time": slot,
            }

        current += timedelta(
            minutes=int(doctor.appointment_duration)
        )

    print("🔥 DEBUG RESULT: NO SLOTS AVAILABLE")

    return {
        "success": False,
        "message": "No slots available."
    }