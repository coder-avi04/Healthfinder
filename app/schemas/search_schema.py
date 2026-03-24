from pydantic import BaseModel

class SearchRequest(BaseModel):
    symptom: str
    location: str
    budget: int