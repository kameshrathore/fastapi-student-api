from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db, engine
from models import Base, StudentMarks, StudentDetails
from schemas import StudentMarksCreate, StudentDetailsCreate
from auth import create_access_token, verify_token, oauth2_scheme, get_user, fake_users_db, verify_password
#Initialized the FastAPI app
app = FastAPI()

# Create all database tables defined by the Base metadata
Base.metadata.create_all(bind=engine)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Authenticate user and create access token
    user = get_user(fake_users_db, form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})  # Generate access token
    return {"access_token": access_token, "token_type": "bearer"}

@app.put("/students/details")
def insert_or_update_student_details(
        student: StudentDetailsCreate,  # Student details to be inserted or updated
        update_flag: bool = Query(False),
        db: Session = Depends(get_db),  # Database session dependency
        token: str = Depends(oauth2_scheme)  # OAuth2 token dependency
):
    # Validate the token
    verify_token(HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials"))

    # Check if a student with the same email already exists
    db_email = db.query(StudentDetails).filter(StudentDetails.email == student.email).first()
    if db_email and (not update_flag or db_email.student_id != student.student_id):
        raise HTTPException(status_code=400, detail="Email already exists")

    # Check if the student already exists in the database
    db_student = db.query(StudentDetails).filter(StudentDetails.student_id == student.student_id).first()
    if db_student:
        if update_flag:
            # Update student details if update_flag is True
            db_student.name = student.name
            db_student.age = student.age
            db_student.email = student.email
            db.commit()
            return {"message": "Student details updated successfully"}
        else:
            raise HTTPException(status_code=400, detail="Student already exists")

    # Insert new student details
    new_student = StudentDetails(**student.dict())
    db.add(new_student)
    db.commit()
    return {"message": "Student details inserted successfully"}

@app.put("/students/marks")
def insert_or_update_student_marks(
        marks: StudentMarksCreate,  # Student marks to be inserted or updated
        update_flag: bool = Query(False),
        db: Session = Depends(get_db),  # Database session dependency
        token: str = Depends(oauth2_scheme)  # OAuth2 token dependency
):
    # Validate the token
    verify_token(HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials"))

    # Check if marks for the student and subject already exist
    db_marks = db.query(StudentMarks).filter(
        StudentMarks.student_id == marks.student_id,
        StudentMarks.subject == marks.subject
    ).first()

    if db_marks:
        if update_flag:
            # Update marks if update_flag is True
            db_marks.marks = marks.marks
            db.commit()
            return {"message": "Student marks updated successfully"}
        else:
            raise HTTPException(status_code=400, detail="Marks already exist for this subject")

    # Insert new marks
    new_marks = StudentMarks(student_id=marks.student_id, subject=marks.subject, marks=marks.marks)
    db.add(new_marks)
    db.commit()
    return {"message": "Student marks inserted successfully"}
