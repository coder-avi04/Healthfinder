from fastapi import APIRouter, HTTPException
from app.utils.db import db
from passlib.context import CryptContext
from app.schemas.user_schema import UserCreate
from app.utils.jwt_handler import create_token
from pydantic import BaseModel

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"])

# ---------------- SIGNUP ----------------
@router.post("/signup")
def signup(user: UserCreate):
    hashed_password = pwd_context.hash(user.password[:72])

    db.users.insert_one({
        "name": user.name,
        "email": user.email,
        "password": hashed_password
    })

    return {"message": "User created ✅"}


# ---------------- LOGIN ----------------
class LoginData(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(data: LoginData):
    user = db.users.find_one({"email": data.email})

    if not user or not pwd_context.verify(data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_token({"user_id": str(user["_id"])})

    return {
        "message": "Login successful ✅",
        "token": token
    }