from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.working_day import WorkingDay
from app.schemas.working_day import WorkingDayCreate, WorkingDayUpdate

router = APIRouter(
    prefix="/working-days",
    tags=["Working Days"]
)


@router.get("/")
def get_working_days(db: Session = Depends(get_db)):
    return db.query(WorkingDay).all()


@router.post("/")
def create_working_day(
    working_day: WorkingDayCreate,
    db: Session = Depends(get_db)
):
    new_working_day = WorkingDay(
        doctor_id=working_day.doctor_id,
        day=working_day.day
    )

    db.add(new_working_day)
    db.commit()
    db.refresh(new_working_day)

    return {
        "message": "Working day added successfully",
        "working_day": new_working_day
    }