from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import RegistrationCreate, RegistrationResponse
import Btap2.service as service
router = APIRouter(tags=["Registrations"])

@router.post(
    "/registrations",response_model=RegistrationResponse,status_code=status.HTTP_201_CREATED
)
def create_registration(
    registration: RegistrationCreate,db: Session = Depends(get_db)
):
    student = service.get_student(db, registration.student_id)
    if not student:
        raise HTTPException(
            status_code=404,detail="Student not found"
        )
    workshop = service.get_workshop(db, registration.workshop_id)
    if not workshop:
        raise HTTPException(
            status_code=404,detail="Workshop not found"
        )
    if student.status != "ACTIVE":
        raise HTTPException(
            status_code=400,detail="Student is inactive"
        )
    if workshop.status != "OPEN":
        raise HTTPException(
            status_code=400,detail="Workshop is closed"
        )
    duplicate = service.check_registration(
        db,registration.student_id,registration.workshop_id
    )
    if duplicate:
        raise HTTPException(
            status_code=400,detail="Student already registered"
        )
    total = service.count_registration(
        db,registration.workshop_id
    )
    if total >= workshop.maximum_participants:
        raise HTTPException(
            status_code=400,detail="Workshop is full"
        )
    return service.create_registration(
        db,registration.student_id,registration.workshop_id
    )

@router.delete("/registrations/{registration_id}")
def delete_registration(
    registration_id: int,db: Session = Depends(get_db)
):
    registration = service.get_registration(db, registration_id)
    if not registration:
        raise HTTPException(
            status_code=404,detail="Registration not found"
        )
    service.delete_registration(db, registration)
    return {
        "message": "Registration cancelled successfully"
    }