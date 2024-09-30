from pydantic import BaseModel

# Schema for inserting and updating student details
class StudentDetailsCreate(BaseModel):
    student_id: int
    name: str
    age: int
    email: str

# Schema for inserting and updating student marks
class StudentMarksCreate(BaseModel):
    student_id: int
    subject: str
    marks: float
