from pydantic import BaseModel
from datetime import datetime

class StudentCreate(BaseModel):
    student_code: str
    full_name: str
    email: str
    status: str

class WorkshopCreate(BaseModel):
    title: str
    description: str
    maximum_participants: int
    status: str
    start_time: datetime

class RegistrationCreate(BaseModel):
    student_id: int
    workshop_id: int