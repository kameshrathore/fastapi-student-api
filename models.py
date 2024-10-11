# Database models representing the structure of tables.
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class StudentDetails(Base):
    __tablename__ = 'student_details2'  # Name of the table in the database
    student_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    email = Column(String, unique=True, index=True)

class StudentMarks(Base):
    __tablename__ = 'student_marks2'  # Name of the table in the database
    student_id = Column(Integer, ForeignKey('student_details2.student_id'), primary_key=True, index=True)  # Foreign key to StudentDetails
    subject = Column(String, primary_key=True, index=True)  # Subject name (part of the primary key)
    marks = Column(Float)

    # Relationship to access StudentDetails from StudentMarks
    student = relationship("StudentDetails")
