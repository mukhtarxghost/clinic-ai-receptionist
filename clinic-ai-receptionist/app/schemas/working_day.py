from pydantic import BaseModel


class WorkingDayCreate(BaseModel):
    doctor_id: int
    day: str


class WorkingDayUpdate(BaseModel):
    day: str