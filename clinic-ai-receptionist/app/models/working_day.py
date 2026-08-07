from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.database import Base


class WorkingDay(Base):
    __tablename__ = "working_days"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    day = Column(String, nullable=False)