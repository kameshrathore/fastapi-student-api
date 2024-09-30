#database models that represent the structure of your tables.
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class StudentDetails(Base):
    __tablename__ = 'student_details2'
    student_id = Column(Integer, primary_key=True, index=True)
    name= Column(String, index=True)
    age = Column(Integer)
    email = Column(String, unique=True, index=True)

class StudentMarks(Base):
    __tablename__ = 'student_marks2'
    student_id = Column(Integer, ForeignKey('student_details2.student_id'), index=True)
    subject = Column(String, primary_key=True)
    marks = Column(Float)

student = relationship("StudentDetails")