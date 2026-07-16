from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import StudentCreate, StudentResponse
import Btap2.service as service
router = APIRouter(tags=["Students"])

@router.post(
    "/students",response_model=StudentResponse,status_code=status.HTTP_201_CREATED
)
def create_student(
    student: StudentCreate,db: Session = Depends(get_db)
):
    return service.create_student(db, student)

@router.get(
    "/students",response_model=list[StudentResponse]
)
def get_students(db: Session = Depends(get_db)):
    return service.get_students(db)
@router.get("/students/{student_id}/workshops")
def get_student_workshops(
    student_id: int,db: Session = Depends(get_db)
):
    student = service.get_student(db, student_id)
    if not student:
        raise HTTPException(
            status_code=404,detail="Student not found"
        )
    registrations = service.get_student_workshops(db, student_id)
    workshops = []
    for registration in registrations:
        workshops.append({
            "id": registration.workshop.id,"title": registration.workshop.title
        })
    return {
        "student_id": student.id,"student_code": student.student_code,"full_name": student.full_name,"workshops": workshops
    }