from fastapi import APIRouter
from app.utils.db import db
from bson import ObjectId

router = APIRouter()

# ✅ Verify doctor
@router.put("/verify-doctor/{doctor_id}")
def verify_doctor(doctor_id: str):
    db.doctors.update_one(
        {"_id": ObjectId(doctor_id)},
        {"$set": {"verified": True}}
    )
    return {"message": "Doctor verified ✅"}


# 👥 Get all users
@router.get("/users")
def get_users():
    users = list(db.users.find())

    for u in users:
        u["_id"] = str(u["_id"])

    return users

@router.delete("/delete-all-users")
def delete_all_users():
    db.users.delete_many({})
    return {"message": "All users deleted ✅"}

# 🎁 Set discount
@router.post("/discount")
def set_discount(value: int):
    return {"discount": value}