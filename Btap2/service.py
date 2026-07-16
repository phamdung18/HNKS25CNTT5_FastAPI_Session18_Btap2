from sqlalchemy.orm import Session
from models import Student, Workshop, Registration

def get_students(db: Session):
    return db.query(Student).all()

def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def create_student(db: Session, student):
    new_student = Student(
        student_code=student.student_code,
        full_name=student.full_name,
        email=student.email,
status=student.status
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

def get_workshops(db: Session):
    return db.query(Workshop).all()

def get_workshop(db: Session, workshop_id: int):
    return db.query(Workshop).filter(
        Workshop.id == workshop_id
    ).first()

def create_workshop(db: Session, workshop):
    new_workshop = Workshop(
        title=workshop.title,description=workshop.description,
        maximum_participants=workshop.maximum_participants,
        status=workshop.status,start_time=workshop.start_time
    )
    db.add(new_workshop)
    db.commit()
    db.refresh(new_workshop)
    return new_workshop

def check_duplicate(db: Session, student_id: int, workshop_id: int):
    return db.query(Registration).filter(
        Registration.student_id == student_id,Registration.workshop_id == workshop_id
    ).first()

def count_registration(db: Session, workshop_id: int):
    return db.query(Registration).filter(
        Registration.workshop_id == workshop_id
    ).count()

def create_registration(db: Session, student_id: int, workshop_id: int):
    registration = Registration(
        student_id=student_id,workshop_id=workshop_id
    )
    db.add(registration)
    db.commit()
    db.refresh(registration)
    return registration

def get_student_workshops(db: Session, student_id: int):
    return db.query(Registration).filter(
        Registration.student_id == student_id
    ).all()

def get_workshop_students(db: Session, workshop_id: int):
    return db.query(Registration).filter(
        Registration.workshop_id == workshop_id
    ).all()

def get_registration(db: Session, registration_id: int):
    return db.query(Registration).filter(
        Registration.id == registration_id
    ).first()

def delete_registration(db: Session, registration):
    db.delete(registration)
    db.commit()