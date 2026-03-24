from fastapi import APIRouter, HTTPException
from app.utils.db import db
from app.schemas.booking_schema import Booking
from bson import ObjectId
from app.utils.email_service import send_email

router = APIRouter()

# 📅 Book appointment (STEP 1: Pending)
@router.post("/")
def create_booking(data: Booking):

    # ✅ Check user exists
    user = db.users.find_one({"_id": ObjectId(data.user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found ❌")

    # ✅ Check doctor exists
    doctor = db.doctors.find_one({"_id": ObjectId(data.doctor_id)})
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found ❌")

    # ✅ Check slot available
    if data.slot not in doctor.get("slots", []):
        raise HTTPException(status_code=400, detail="Invalid slot ❌")

    # ✅ Check slot already booked
    existing = db.bookings.find_one({
        "doctor_id": data.doctor_id,
        "slot": data.slot,
        "status": {"$in": ["pending", "confirmed"]}
    })

    if existing:
        raise HTTPException(status_code=400, detail="Slot already booked ❌")

    # ✅ Discount logic
    discount = 10
    existing_booking = db.bookings.find_one({"user_id": data.user_id})
    if not existing_booking:
        discount = 15

    booking = {
        "user_id": data.user_id,
        "doctor_id": data.doctor_id,
        "slot": data.slot,
        "status": "pending",   # 🔥 IMPORTANT CHANGE
        "payment_status": "pending",
        "discount": discount
    }

    result = db.bookings.insert_one(booking)

    # 📩 Email to USER (pending)
    try:
        send_email(
            user["email"],
            "Booking in Progress ⏳",
            f"Your appointment request with {doctor['name']} at {data.slot} is pending approval."
        )
    except:
        print("User email failed")

    # 📩 Email to DOCTOR (new request)
    try:
        send_email(
            doctor.get("email", user["email"]),  # fallback
            "New Appointment Request 📅",
            f"You have a new appointment request at {data.slot}"
        )
    except:
        print("Doctor email failed")

    return {
        "message": "Booking request sent ⏳",
        "booking_id": str(result.inserted_id),
        "status": "pending"
    }


# ✅ Confirm booking (STEP 2: Doctor/Admin approves)
@router.put("/{booking_id}/confirm")
def confirm_booking(booking_id: str):

    booking = db.bookings.find_one({"_id": ObjectId(booking_id)})
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found ❌")

    # update status
    db.bookings.update_one(
        {"_id": ObjectId(booking_id)},
        {"$set": {"status": "confirmed"}}
    )

    # get user + doctor
    user = db.users.find_one({"_id": ObjectId(booking["user_id"])})
    doctor = db.doctors.find_one({"_id": ObjectId(booking["doctor_id"])})

    # 📩 Email to USER (confirmed)
    try:
        send_email(
            user["email"],
            "Appointment Confirmed ✅",
            f"Your appointment with {doctor['name']} at {booking['slot']} is confirmed."
        )
    except:
        print("Confirmation email failed")

    return {"message": "Booking confirmed ✅"}


# 📋 Get user bookings
@router.get("/user/{user_id}")
def get_bookings(user_id: str):
    bookings = list(db.bookings.find({"user_id": user_id}))

    for b in bookings:
        b["_id"] = str(b["_id"])
        b["doctor_id"] = str(b["doctor_id"])

    return bookings


# 🔍 Get booking by ID
@router.get("/{booking_id}")
def get_booking(booking_id: str):
    booking = db.bookings.find_one({"_id": ObjectId(booking_id)})

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found ❌")

    booking["_id"] = str(booking["_id"])
    booking["doctor_id"] = str(booking["doctor_id"])

    return booking


@router.put("/{booking_id}/confirm")
def confirm_booking(booking_id: str):

    booking = db.bookings.find_one({"_id": ObjectId(booking_id)})
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found ❌")

    # update status
    db.bookings.update_one(
        {"_id": ObjectId(booking_id)},
        {"$set": {"status": "confirmed"}}
    )

    # get user + doctor
    user = db.users.find_one({"_id": ObjectId(booking["user_id"])})
    doctor = db.doctors.find_one({"_id": ObjectId(booking["doctor_id"])})

    # 📩 Email to USER
    try:
        send_email(
            user["email"],
            "Appointment Confirmed ✅",
            f"Your appointment with {doctor['name']} at {booking['slot']} is confirmed."
        )
    except:
        print("Email failed")

    return {"message": "Booking confirmed ✅"}

# ❌ Cancel booking
@router.put("/{booking_id}/cancel")
def cancel_booking(booking_id: str):
    result = db.bookings.update_one(
        {"_id": ObjectId(booking_id)},
        {"$set": {"status": "cancelled"}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Booking not found ❌")

    return {"message": "Booking cancelled ❌"}


# ✅ Complete booking
@router.put("/{booking_id}/complete")
def complete_booking(booking_id: str):
    db.bookings.update_one(
        {"_id": ObjectId(booking_id)},
        {"$set": {"status": "completed"}}
    )

    return {"message": "Booking completed ✅"}