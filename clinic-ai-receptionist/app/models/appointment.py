from sqlalchemy import Column, Integer, String
from app.database.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    doctor = Column(String(255), nullable=False)
    date = Column(String(20), nullable=False)
    time = Column(String(20), nullable=False)