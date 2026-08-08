from sqlalchemy import Column, Integer, String
from app.database.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False)
    specialization = Column(String(255), nullable=False)

    start_time = Column(String(20), nullable=False)
    end_time = Column(String(20), nullable=False)

    appointment_duration = Column(Integer, nullable=False, default=20)