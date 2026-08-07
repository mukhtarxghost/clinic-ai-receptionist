from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorCreate, DoctorUpdate
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

    db.commit()
    db.refresh(doctor)

    return {
        "message": "Doctor updated successfully",
        "doctor": doctor
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

@router.post("/")
def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db)
):
    new_doctor = Doctor(
        name=doctor.name,
        specialization=doctor.specialization,
        start_time=doctor.start_time,
        end_time=doctor.end_time
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
            "end_time": new_doctor.end_time
        }
    }