from fastapi import FastAPI

from app.routes import health, appointments, doctors
from app.database.database import Base, engine
from app.models.appointment import Appointment
from app.models.doctor import Doctor

app = FastAPI()

# Create all database tables
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(health.router)
app.include_router(appointments.router)
app.include_router(doctors.router)