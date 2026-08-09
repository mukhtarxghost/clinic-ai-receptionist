from fastapi import FastAPI

from app.routes import health, appointments, doctors
from app.database.database import Base, engine
from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.working_day import WorkingDay
from app.routes import health, appointments, doctors, working_days
from app.models.doctor_leave import DoctorLeave
from app.routes import health, appointments, doctors, working_days, chat


app = FastAPI()
from app.routes.webhook import router as webhook_router

app.include_router(webhook_router)

# Create all database tables
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(health.router)
app.include_router(appointments.router)
app.include_router(doctors.router)
app.include_router(working_days.router)
app.include_router(chat.router)