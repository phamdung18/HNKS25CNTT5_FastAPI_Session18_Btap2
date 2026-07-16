from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from schemas import StudentCreate, WorkshopCreate, RegistrationCreate
import Btap2.service as service
Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.post("/students", status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    return service.create_student(db, student)
@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    return service.get_students(db)
@app.post("/workshops", status_code=201)
def create_workshop(workshop: WorkshopCreate, db: Session = Depends(get_db)):
    return service.create_workshop(db, workshop)
@app.get("/workshops")
def get_workshops(db: Session = Depends(get_db)):
    return service.get_workshops(db)
@app.get("/workshops/{workshop_id}")
def get_workshop(workshop_id: int, db: Session = Depends(get_db)):
    workshop = service.get_workshop(db, workshop_id)
    if workshop is None:
        raise HTTPException(status_code=404, detail="Workshop not found")
    return workshop
@app.post("/registrations", status_code=201)
def create_registration(
    registration: RegistrationCreate,db: Session = Depends(get_db)
):
    student = service.get_student(db, registration.student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    workshop = service.get_workshop(db, registration.workshop_id)
    if workshop is None:
        raise HTTPException(status_code=404, detail="Workshop not found")
    if student.status != "ACTIVE":
        raise HTTPException(status_code=400, detail="Student is inactive")
    if workshop.status != "OPEN":
        raise HTTPException(status_code=400, detail="Workshop is closed")
    check = service.check_duplicate(
        db,registration.student_id,registration.workshop_id
    )
    if check:
        raise HTTPException(
            status_code=400,detail="Student already registered"
        )
    total = service.count_registration(db, registration.workshop_id)
    if total >= workshop.maximum_participants:
        raise HTTPException(
            status_code=400,detail="Workshop is full"
        )
    return service.create_registration(
        db,registration.student_id,registration.workshop_id
    )

@app.get("/students/{student_id}/workshops")
def get_student_workshops(
    student_id: int,db: Session = Depends(get_db)
):
    student = service.get_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    registrations = service.get_student_workshops(db, student_id)
    workshops = []
    for item in registrations:
        workshops.append({
            "id": item.workshop.id,"title": item.workshop.title
        })
    return {
        "student_id": student.id,"full_name": student.full_name,"workshops": workshops
    }
@app.get("/workshops/{workshop_id}/students")
def get_workshop_students(
    workshop_id: int,db: Session = Depends(get_db)
):
    workshop = service.get_workshop(db, workshop_id)
    if workshop is None:
        raise HTTPException(status_code=404, detail="Workshop not found")
    registrations = service.get_workshop_students(db, workshop_id)
    students = []
    for item in registrations:
        students.append({
            "id": item.student.id,"student_code": item.student.student_code,"full_name": item.student.full_name
        })
    return {
        "workshop_id": workshop.id,"title": workshop.title,"students": students
    }
@app.delete("/registrations/{registration_id}")
def delete_registration(
    registration_id: int,db: Session = Depends(get_db)
):
    registration = service.get_registration(db, registration_id)
    if registration is None:
        raise HTTPException(
            status_code=404,detail="Registration not found"
        )
    service.delete_registration(db, registration)
    return {
        "message": "Registration deleted successfully"
    }