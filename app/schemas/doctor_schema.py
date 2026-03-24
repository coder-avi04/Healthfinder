from pydantic import BaseModel
from typing import List

class Doctor(BaseModel):
    name: str
    specialization: str
    experience: int
    fees: int
    location: str
    slots: List[str]