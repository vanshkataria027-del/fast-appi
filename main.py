from pathlib import Path
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session 
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from database import engine,SessionLocal,  Base 
from models import StudentDB
app = FastAPI()

import os
BASE_DIR =  Path(__file__).resolve().parent

class StudentResponse(BaseModel):
      name: str
      age: int

Base.metadata.create_all(bind=engine)
def get_db():
      db = SessionLocal()
      try:
            yield db
      finally:
            db.close()
class Student(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(gt=0, lt=100)
    grade: float = Field(ge= 0, le=10)

@app.get("/")
def home():
      return {"message": "Welcome! Server working!"}
@app.post("/students/")
def create_student(student: Student, db: Session = Depends(get_db)):
    new_student = StudentDB(name=student.name, age=student.age, grade=student.grade)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@app.get("/students/")
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(StudentDB).all()
    return students

@app.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student, db: Session = Depends(get_db)):
    db_student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    db_student.name = student.name
    db_student.age = student.age
    db_student.grade = student.grade
    db.commit()
    db.refresh(db_student)
    return db_student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted"}
class StudentResponse(BaseModel):
     
     name: str
     age: int

    
@app.post("/students" , response_model=StudentResponse)
def create_student(student: Student, db: Session = Depends(get_db)):
        new_student = StudentDB(name=student.name,  age=student.age, grade=student.grade)
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return new_student

@app.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentDB).filter(StudentDB.id== student_id).first()
    if not student:
          raise HTTPException(status_code=404, detail="Student not found")
    return {"id": student.id, "name": student.name, "age": student.age, "grade": student.grade}