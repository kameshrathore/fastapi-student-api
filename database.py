from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import db_params

# Database connection URL
DATABASE_URL = f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)  # Engine for managing database connections
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Session factory for database sessions
Base = declarative_base()  # Base class for ORM models

# Dependency function to get a database session
def get_db():
    db = SessionLocal()  # Create a new session
    try:
        yield db  # Provide the session for use
    finally:
        db.close()  # Close the session when done
