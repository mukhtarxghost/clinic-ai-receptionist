from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate
from app.services.appointment_service import book_appointment


router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


@router.get("/")
def get_appointments(db: Session = Depends(get_db)):
    appointments = db.query(Appointment).all()
    return appointments

@router.get("/phone/{phone}")
def get_appointments_by_phone(
    phone: str,
    db: Session = Depends(get_db)
):
    appointments = db.query(Appointment).filter(
        Appointment.phone == phone
    ).all()

    if not appointments:
        return {
            "message": "No appointments found for this phone number"
        }

    return appointments

@router.get("/doctor/{doctor}")
def get_doctor_schedule(
    doctor: str,
    db: Session = Depends(get_db)
):
    appointments = (
        db.query(Appointment)
        .filter(Appointment.doctor == doctor)
        .all()
    )

    if not appointments:
        return {
            "message": "No appointments found for this doctor"
        }

    return appointments

@router.get("/check")
def check_slot_availability(
    doctor: str,
    date: str,
    time: str,
    db: Session = Depends(get_db)
):
    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.doctor == doctor,
            Appointment.date == date,
            Appointment.time == time
        )
        .first()
    )

    if appointment:
        return {
            "available": False,
            "message": "Slot already booked"
        }

    return {
        "available": True,
        "message": "Slot available"
    }

@router.post("/")
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db)
):
    result = book_appointment(
        db=db,
        patient_name=appointment.patient_name,
        phone=appointment.phone,
        doctor_name=appointment.doctor,
        date=appointment.date,
        time=appointment.time
    )

    return result

@router.put("/{appointment_id}")
def update_appointment(
    appointment_id: int,
    updated: AppointmentUpdate,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if appointment is None:
        return {
            "message": "Appointment not found"
        }

    appointment.patient_name = updated.patient_name
    appointment.phone = updated.phone
    appointment.doctor = updated.doctor
    appointment.date = updated.date
    appointment.time = updated.time

    db.commit()
    db.refresh(appointment)

    return {
        "message": "Appointment updated successfully",
        "appointment": {
            "id": appointment.id,
            "patient_name": appointment.patient_name,
            "phone": appointment.phone,
            "doctor": appointment.doctor,
            "date": appointment.date,
            "time": appointment.time
        }
    }

@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if appointment is None:
        return {
            "message": "Appointment not found"
        }

    db.delete(appointment)
    db.commit()

    return {
        "message": "Appointment deleted successfully"
    }