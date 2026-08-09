from fastapi import FastAPI

from app.database.database import Base, engine

from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.working_day import WorkingDay
from app.models.doctor_leave import DoctorLeave

from app.routes import (
    health,
    appointments,
    doctors,
    working_days,
    chat,
    webhook,
)

app = FastAPI(
    title="Clinic AI Receptionist API",
    version="1.0.0",
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(health.router)
app.include_router(appointments.router)
app.include_router(doctors.router)
app.include_router(working_days.router)
app.include_router(chat.router)
app.include_router(webhook.router)