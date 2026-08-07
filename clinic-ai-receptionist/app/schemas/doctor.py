from pydantic import BaseModel

class DoctorCreate(BaseModel):
    name: str
    specialization: str
    start_time: str
    end_time: str

class DoctorUpdate(BaseModel):
    name: str
    specialization: str
    start_time: str
    end_time: str