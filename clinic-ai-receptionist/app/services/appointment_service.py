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