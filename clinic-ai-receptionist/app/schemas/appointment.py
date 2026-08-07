from pydantic import BaseModel


class AppointmentCreate(BaseModel):
    patient_name: str
    phone: str
    doctor: str
    date: str
    time: str

class AppointmentUpdate(BaseModel):
    patient_name: str
    phone: str
    doctor: str
    date: str
    time: str   