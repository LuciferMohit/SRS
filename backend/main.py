from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel
import os

# Database Setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:root@localhost:5432/student_registration")
engine = create_engine(DATABASE_URL)
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

app = FastAPI()

@app.on_event("startup")
def startup_event():
    """Create tables on startup"""
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Warning: Could not create tables on startup: {e}")

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

@app.post("/students/")
def register_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = StudentDB(name=student.name, email=student.email, course=student.course)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/")
def get_students(db: Session = Depends(get_db)):
    return db.query(StudentDB).order_by(StudentDB.id.desc()).all()