from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.doctor_leave import DoctorLeave


def book_appointment(
    db: Session,
    patient_name: str,
    phone: str,
    doctor_name: str,
    date: str,
    time: str
):
    doctor = db.query(Doctor).filter(
        Doctor.name == doctor_name
    ).first()

    if doctor is None:
        return {
            "success": False,
            "message": "Doctor not found."
        }

    leave = db.query(DoctorLeave).filter(
        DoctorLeave.doctor_id == doctor.id,
        DoctorLeave.date == date
    ).first()

    if leave:
        return {
            "success": False,
            "message": "Doctor is on leave."
        }

    existing = db.query(Appointment).filter(
        Appointment.doctor == doctor_name,
        Appointment.date == date,
        Appointment.time == time
    ).first()

    if existing:
        return {
            "success": False,
            "message": "Slot already booked."
        }

    appointment = Appointment(
        patient_name=patient_name,
        phone=phone,
        doctor=doctor_name,
        date=date,
        time=time
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return {
        "success": True,
        "appointment": "Appointment created successfully"
    }


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
        query = query.filter(
            Appointment.date == date
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

def reschedule_appointment(
    db: Session,
    phone: str,
    doctor_name: str,
    old_date: str,
    old_time: str,
    new_date: str,
    new_time: str,
):
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

    leave = db.query(DoctorLeave).filter(
        DoctorLeave.doctor_id == doctor.id,
        DoctorLeave.date == new_date
    ).first()

    if leave:
        return {
            "success": False,
            "message": "Doctor is on leave on the requested date."
        }

    existing = db.query(Appointment).filter(
        Appointment.doctor == doctor_name,
        Appointment.date == new_date,
        Appointment.time == new_time,
    ).first()

    if existing:
        return {
            "success": False,
            "message": "Requested slot is already booked."
        }

    appointment.date = new_date
    appointment.time = new_time

    db.commit()
    db.refresh(appointment)

    return {
        "success": True,
        "message": "Appointment rescheduled successfully."
    }

from datetime import datetime, timedelta


def get_next_available_slot(
    db: Session,
    doctor_name: str,
    date: str,
):
    doctor = db.query(Doctor).filter(
        Doctor.name == doctor_name
    ).first()

    if doctor is None:
        return {
            "success": False,
            "message": "Doctor not found."
        }

    leave = db.query(DoctorLeave).filter(
        DoctorLeave.doctor_id == doctor.id,
        DoctorLeave.date == date
    ).first()

    if leave:
        return {
            "success": False,
            "message": "Doctor is on leave."
        }

    booked = db.query(Appointment).filter(
        Appointment.doctor == doctor_name,
        Appointment.date == date
    ).all()

    booked_slots = {
        appointment.time
        for appointment in booked
    }

    current = datetime.strptime(
        doctor.start_time,
        "%H:%M"
    )

    end = datetime.strptime(
        doctor.end_time,
        "%H:%M"
    )

    while current < end:

        slot = current.strftime("%H:%M")

        if slot not in booked_slots:
            return {
                "success": True,
                "date": date,
                "time": slot
            }

        current += timedelta(
            minutes=doctor.appointment_duration
        )

    return {
        "success": False,
        "message": "No slots available."
    }