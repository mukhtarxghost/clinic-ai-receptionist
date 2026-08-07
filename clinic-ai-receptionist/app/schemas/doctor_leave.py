from pydantic import BaseModel


class DoctorLeaveCreate(BaseModel):
    date: str
    reason: str