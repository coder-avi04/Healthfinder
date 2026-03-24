from pydantic import BaseModel

class Booking(BaseModel):
    user_id: str
    doctor_id: str
    slot: str