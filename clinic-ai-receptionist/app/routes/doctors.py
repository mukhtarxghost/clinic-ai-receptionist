from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorCreate, DoctorUpdate
from app.models.appointment import Appointment
from app.models.doctor_leave import DoctorLeave
from app.schemas.doctor_leave import DoctorLeaveCreate


router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


@router.get("/")
def get_doctors(db: Session = Depends(get_db)):
    return db.query(Doctor).all()


@router.get("/{doctor_id}")
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if doctor is None:
        return {
            "message": "Doctor not found"
        }

    return doctor

@router.get("/{doctor_id}/slots")
def get_doctor_slots(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if doctor is None:
        return {
            "message": "Doctor not found"
        }

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

    return {
        "doctor": doctor.name,
        "slots": slots
    }

@router.get("/{doctor_id}/next-available")
def get_next_available_slot(
    doctor_id: int,
    date: str,
    db: Session = Depends(get_db)
):
    # Check if doctor exists
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if doctor is None:
        return {
            "message": "Doctor not found"
        }

    # Check if doctor is on leave
    leave = db.query(DoctorLeave).filter(
        DoctorLeave.doctor_id == doctor_id,
        DoctorLeave.date == date
    ).first()

    if leave:
        return {
            "doctor": doctor.name,
            "date": date,
            "message": "Doctor is on leave",
            "reason": leave.reason
        }

    # Generate all possible slots
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

    # Fetch booked appointments
    appointments = db.query(Appointment).filter(
        Appointment.doctor == doctor.name,
        Appointment.date == date
    ).all()

    booked_slots = [
        appointment.time
        for appointment in appointments
    ]

    # Find first available slot
    for slot in slots:
        if slot not in booked_slots:
            return {
                "doctor": doctor.name,
                "date": date,
                "next_available_slot": slot
            }

    return {
        "doctor": doctor.name,
        "date": date,
        "message": "No slots available"
    }



@router.post("/")
def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db)
):
    new_doctor = Doctor(
        name=doctor.name,
        specialization=doctor.specialization,
        start_time=doctor.start_time,
        end_time=doctor.end_time,
        appointment_duration=doctor.appointment_duration
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return {
        "message": "Doctor created successfully",
        "doctor": {
            "id": new_doctor.id,
            "name": new_doctor.name,
            "specialization": new_doctor.specialization,
            "start_time": new_doctor.start_time,
            "end_time": new_doctor.end_time,
            "appointment_duration": new_doctor.appointment_duration
        }
    }


@router.put("/{doctor_id}")
def update_doctor(
    doctor_id: int,
    updated: DoctorUpdate,
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if doctor is None:
        return {
            "message": "Doctor not found"
        }

    doctor.name = updated.name
    doctor.specialization = updated.specialization
    doctor.start_time = updated.start_time
    doctor.end_time = updated.end_time
    doctor.appointment_duration = updated.appointment_duration

    db.commit()
    db.refresh(doctor)

    return {
        "message": "Doctor updated successfully",
        "doctor": {
            "id": doctor.id,
            "name": doctor.name,
            "specialization": doctor.specialization,
            "start_time": doctor.start_time,
            "end_time": doctor.end_time,
            "appointment_duration": doctor.appointment_duration
        }
    }


@router.delete("/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if doctor is None:
        return {
            "message": "Doctor not found"
        }

    db.delete(doctor)
    db.commit()

    return {
        "message": "Doctor deleted successfully"
    }

@router.post("/{doctor_id}/leave")
def add_doctor_leave(
    doctor_id: int,
    leave: DoctorLeaveCreate,
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if doctor is None:
        return {
            "message": "Doctor not found"
        }

    new_leave = DoctorLeave(
        doctor_id=doctor_id,
        date=leave.date,
        reason=leave.reason
    )

    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)

    return {
        "message": "Leave added successfully",
        "leave": {
            "doctor_id": doctor_id,
            "date": new_leave.date,
            "reason": new_leave.reason
        }
    }