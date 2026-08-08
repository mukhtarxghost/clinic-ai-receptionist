from sqlalchemy import Column, Integer, String
from app.database.database import Base


class DoctorLeave(Base):
    __tablename__ = "doctor_leaves"

    id = Column(Integer, primary_key=True, index=True)

    doctor_id = Column(Integer, nullable=False)

    date = Column(String(20), nullable=False)
    reason = Column(String(255), nullable=False)