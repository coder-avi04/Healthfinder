from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Doctor Finder Backend Running 🚀"}

from app.utils.db import db

@app.get("/test-db")
def test_db():
    return {"collections": db.list_collection_names()}

from app.routes import auth

app.include_router(auth.router, prefix="/auth")

from app.routes import doctor

app.include_router(doctor.router, prefix="/doctors")

from app.routes import booking

app.include_router(booking.router, prefix="/bookings")

from app.routes import admin

app.include_router(admin.router, prefix="/admin")