from sqlalchemy.orm import Session

from app.models.doctor import Doctor


from sqlalchemy.orm import Session

from app.models.doctor import Doctor
from app.models.appointment import Appointment


def get_all_doctors(db: Session):
    doctors = db.query(Doctor).all()

    return [
        {
            "id": doctor.id,
            "name": doctor.name,
            "specialization": doctor.specialization,
            "start_time": doctor.start_time,
            "end_time": doctor.end_time,
            "appointment_duration": doctor.appointment_duration,
        }
        for doctor in doctors
    ]


def get_doctor_by_name(
    db: Session,
    doctor_name: str
):
    doctor = db.query(Doctor).filter(
        Doctor.name == doctor_name
    ).first()

    if doctor is None:
        return None

    return {
        "id": doctor.id,
        "name": doctor.name,
        "specialization": doctor.specialization,
        "start_time": doctor.start_time,
        "end_time": doctor.end_time,
        "appointment_duration": doctor.appointment_duration,
    }


def get_patient_appointments(
    db: Session,
    phone: str
):
    appointments = db.query(Appointment).filter(
        Appointment.phone == phone
    ).all()

    return [
        {
            "id": appointment.id,
            "patient_name": appointment.patient_name,
            "doctor": appointment.doctor,
            "date": appointment.date,
            "time": appointment.time,
        }
        for appointment in appointments
    ]


AVAILABLE_TOOLS = {
    "get_all_doctors": get_all_doctors,
    "get_doctor_by_name": get_doctor_by_name,
    "get_patient_appointments": get_patient_appointments,
}