from sqlalchemy import Column, Integer, String
from app.database.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    doctor = Column(String, nullable=False)
    date = Column(String, nullable=False)
    time = Column(String, nullable=False)