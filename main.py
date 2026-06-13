from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import engine,SessionLocal,  Base 
from models import StudentDB
app = FastAPI()

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

class StudentResponse(BaseModel):
     name: str
     age: int

@app.get("/")
def home():
        return {"message": "Hello World"}
    
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