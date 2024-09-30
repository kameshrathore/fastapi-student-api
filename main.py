from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm  # Add this line
from sqlalchemy.orm import Session
from database import get_db, engine
from models import Base, StudentMarks, StudentDetails
from schemas import StudentMarksCreate, StudentDetailsCreate
from auth import create_access_token, verify_token, oauth2_scheme, get_user, fake_users_db, verify_password

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(fake_users_db, form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.put("/students/details")
def insert_or_update_student_details(
        student: StudentDetailsCreate,
        update_flag: bool = Query(False),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):
    # Validate the token
    verify_token(HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials"))

    db_student = db.query(StudentDetails).filter(StudentDetails.student_id == student.student_id).first()
    if db_student:
        if update_flag:
            db_student.name = student.name
            db_student.age = student.age
            db_student.email = student.email
            db.commit()
            return {"message": "Student details updated successfully"}
        else:
            raise HTTPException(status_code=400, detail="Student already exists")

    new_student = StudentDetails(**student.dict())
    db.add(new_student)
    db.commit()
    return {"message": "Student details inserted successfully"}

@app.put("/students/marks")
def insert_or_update_student_marks(
        marks: StudentMarksCreate,
        update_flag: bool = Query(False),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):
    # Validate the token
    verify_token(HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials"))

    db_marks = db.query(StudentMarks).filter(
        StudentMarks.student_id == marks.student_id,
        StudentMarks.subject == marks.subject
    ).first()

    if db_marks:
        if update_flag:
            db_marks.marks = marks.marks
            db.commit()
            return {"message": "Student marks updated successfully"}
        else:
            raise HTTPException(status_code=400, detail="Marks already exist for this subject")

    new_marks = StudentMarks(student_id=marks.student_id, subject=marks.subject, marks=marks.marks)
    db.add(new_marks)
    db.commit()
    return {"message": "Student marks inserted successfully"}
