from sqlalchemy import Column, Integer, String, Float
from database import Base

class StudentDB(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, index=True)
    name =Column(String, index=True)
    age = Column(Integer)
    grade = Column(Float)