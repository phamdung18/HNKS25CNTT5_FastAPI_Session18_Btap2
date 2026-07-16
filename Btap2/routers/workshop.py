from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import WorkshopCreate, WorkshopResponse
import Btap2.service as service
router = APIRouter(tags=["Workshops"])

@router.post(
    "/workshops",
    response_model=WorkshopResponse,status_code=status.HTTP_201_CREATED
)
def create_workshop(
    workshop: WorkshopCreate,db: Session = Depends(get_db)
):
    return service.create_workshop(db, workshop)

@router.get(
    "/workshops",response_model=list[WorkshopResponse]
)
def get_workshops(
    db: Session = Depends(get_db)
):
    return service.get_workshops(db)
@router.get(
    "/workshops/{workshop_id}",response_model=WorkshopResponse
)
def get_workshop(
    workshop_id: int,db: Session = Depends(get_db)
):
    workshop = service.get_workshop(db, workshop_id)
    if not workshop:
        raise HTTPException(
            status_code=404,detail="Workshop not found"
        )
    return workshop

@router.get("/workshops/{workshop_id}/students")
def get_workshop_students(
    workshop_id: int,db: Session = Depends(get_db)
):
    workshop = service.get_workshop(db, workshop_id)
    if not workshop:
        raise HTTPException(
            status_code=404,detail="Workshop not found"
        )
    registrations = service.get_workshop_students(db, workshop_id)
    students = []
    for registration in registrations:
        students.append({
            "id": registration.student.id,"student_code": registration.student.student_code,"full_name": registration.student.full_name
        })

    return {
        "workshop_id": workshop.id,"title": workshop.title,"students": students
    }