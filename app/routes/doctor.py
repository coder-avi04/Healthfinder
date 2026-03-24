from fastapi import APIRouter
from app.utils.db import db
from app.schemas.doctor_schema import Doctor

router = APIRouter()

# Add doctor
@router.post("/add")
def add_doctor(doctor: Doctor):
    db.doctors.insert_one({
    **doctor.dict(),
    "verified": False
})
    return {"message": "Doctor added ✅"}

# Get all doctors
@router.get("/")
def get_doctors():
    doctors = list(db.doctors.find())
    
    for d in doctors:
        d["_id"] = str(d["_id"])
    
    return doctors

# Get doctor by ID
@router.get("/{id}")
def get_doctor(id: str):
    from bson import ObjectId
    doctor = db.doctors.find_one({"_id": ObjectId(id)})
    
    if doctor:
        doctor["_id"] = str(doctor["_id"])
        return doctor
    
    return {"message": "Doctor not found ❌"}

from app.schemas.search_schema import SearchRequest

# 🔍 Search + Recommendation
@router.post("/search")
def search_doctors(data: SearchRequest):
    doctors = list(db.doctors.find({
        "location": data.location,
        "fees": {"$lte": data.budget}
    }))

    result = []

    for d in doctors:
        # simple scoring logic
        score = (d.get("experience", 0) * 0.5) + (1000 - d.get("fees", 0)) * 0.01
        
        d["_id"] = str(d["_id"])
        d["score"] = round(score, 2)

        result.append(d)

    # sort by score
    result = sorted(result, key=lambda x: x["score"], reverse=True)

    return {
        "recommended": result[:3]
    }