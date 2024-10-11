from pydantic import BaseModel, EmailStr
# Schema for inserting and updating student details
class StudentDetailsCreate(BaseModel):
    student_id: int
    name: str
    age: int
    email: EmailStr # Student's email (validated as a proper email format)

# Schema for inserting and updating student marks
class StudentMarksCreate(BaseModel):
    student_id: int
    subject: str
    marks: float
