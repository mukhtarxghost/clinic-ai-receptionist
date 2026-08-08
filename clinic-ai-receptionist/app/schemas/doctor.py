from pydantic import BaseModel

class DoctorCreate(BaseModel):
    name: str
    specialization: str
    start_time: str
    end_time: str
    appointment_duration: int

class DoctorUpdate(BaseModel):
    name: str
    specialization: str
    start_time: str
    end_time: str
    appointment_duration: int
    