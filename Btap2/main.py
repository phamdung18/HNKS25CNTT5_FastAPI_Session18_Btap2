from fastapi import FastAPI
from database import Base, engine
from routers.student import router as student_router
from routers.workshop import router as workshop_router
from routers.registration import router as registration_router

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Workshop Registration API")
app.include_router(student_router)
app.include_router(workshop_router)
app.include_router(registration_router)