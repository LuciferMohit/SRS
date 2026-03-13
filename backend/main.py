"""Student Registration System API"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel
import os
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database Setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:root@localhost:5433/student_registration")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Model
class StudentDB(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    course = Column(String)

# Pydantic Schema for Data Validation
class StudentCreate(BaseModel):
    name: str
    email: str
    course: str

class Student(StudentCreate):
    id: int
    
    class Config:
        from_attributes = True

app = FastAPI(
    title="Student Registration System",
    description="API for managing student registrations",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    """Create tables on startup"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.warning(f"Warning: Could not create tables on startup: {e}")

# Allow our frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["Health"])
def root():
    """Health check endpoint"""
    return {"status": "API is running", "version": "1.0.0"}

@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

@app.post("/students/", response_model=Student, tags=["Students"])
def register_student(student: StudentCreate, db: Session = Depends(get_db)):
    """Register a new student"""
    try:
        db_student = StudentDB(name=student.name, email=student.email, course=student.course)
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        logger.info(f"Student registered: {student.email}")
        return db_student
    except Exception as e:
        db.rollback()
        logger.error(f"Error registering student: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/students/", response_model=List[Student], tags=["Students"])
def get_students(db: Session = Depends(get_db)):
    """Get all registered students"""
    try:
        students = db.query(StudentDB).order_by(StudentDB.id.desc()).all()
        return students
    except Exception as e:
        logger.error(f"Error fetching students: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/students/{student_id}", response_model=Student, tags=["Students"])
def get_student(student_id: int, db: Session = Depends(get_db)):
    """Get a specific student by ID"""
    try:
        student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
    except Exception as e:
        logger.error(f"Error fetching student: {e}")
        raise

@app.delete("/students/{student_id}", tags=["Students"])
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """Delete a student by ID"""
    try:
        student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        db.delete(student)
        db.commit()
        logger.info(f"Student deleted: {student_id}")
        return {"message": f"Student {student_id} deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting student: {e}")
        raise HTTPException(status_code=400, detail=str(e))