from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate
from app.models.doctor import Doctor
from app.models.doctor_leave import DoctorLeave
from datetime import datetime, timedelta


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
    # Check if doctor exists
    doctor = db.query(Doctor).filter(
        Doctor.name == appointment.doctor
    ).first()

    if doctor is None:
        return {
            "success": False,
            "message": "Doctor not found."
        }

    # Check if doctor is on leave
    leave = db.query(DoctorLeave).filter(
        DoctorLeave.doctor_id == doctor.id,
        DoctorLeave.date == appointment.date
    ).first()

    if leave:
        return {
            "success": False,
            "message": "Doctor is on leave.",
            "reason": leave.reason
        }

    # Generate valid slots
    slots = []

    current = datetime.strptime(
        doctor.start_time,
        "%H:%M"
    )

    end = datetime.strptime(
        doctor.end_time,
        "%H:%M"
    )

    while current < end:
        slots.append(
            current.strftime("%H:%M")
        )

        current += timedelta(
            minutes=doctor.appointment_duration
        )

    # Check if requested time is valid
    if appointment.time not in slots:
        return {
            "success": False,
            "message": "Invalid appointment time.",
            "valid_slots": slots
        }

    # Check if the doctor already has an appointment
    existing_appointment = db.query(Appointment).filter(
        Appointment.doctor == appointment.doctor,
        Appointment.date == appointment.date,
        Appointment.time == appointment.time
    ).first()

    if existing_appointment:
        return {
            "success": False,
            "message": "This slot is already booked for this doctor."
        }

    # Create appointment
    new_appointment = Appointment(
        patient_name=appointment.patient_name,
        phone=appointment.phone,
        doctor=appointment.doctor,
        date=appointment.date,
        time=appointment.time
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return {
        "success": True,
        "message": "Appointment created successfully",
        "appointment": {
            "id": new_appointment.id,
            "patient_name": new_appointment.patient_name,
            "phone": new_appointment.phone,
            "doctor": new_appointment.doctor,
            "date": new_appointment.date,
            "time": new_appointment.time
        }
    }

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