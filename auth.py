from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

# Constants for JWT authentication
SECRET_KEY = "secret_key"  # Secret key for encoding and decoding JWT tokens
ALGORITHM = "HS256"  # Algorithm used for encoding JWT tokens
ACCESS_TOKEN_EXPIRE_MINUTES = 40

# Password hashing context setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # Use bcrypt for password hashing

# OAuth2 password bearer setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # URL for obtaining the token

# Dummy user
fake_users_db = {
    "kamesh18": {
        "username": "kamesh18",
        "full_name": "Kamesh",
        "email": "kamesh18@example.com",
        "hashed_password": pwd_context.hash("password"),
        "disabled": False,  # Indicates if the user is disabled
    }
}

# Function to verify a plain password against a hashed password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to hash a plain password
def get_password_hash(password):
    return pwd_context.hash(password)

# Function to retrieve a user from the database by username
def get_user(db, username: str):
    if username in db:
        return db[username]
    return None

# Function to verify the JWT token
def verify_token(credentials_exception):
    def verify_token(token: str = Depends(oauth2_scheme)):  # Use the OAuth2 scheme to get the token
        credentials = None
        try:
            # Decode the token and extract the username
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # Decode the JWT using the secret key
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception  # Raise an exception if no username is found
            token_data = {"username": username}
        except JWTError:
            raise credentials_exception  # Raise an exception if token verification fails
        return token_data
    return verify_token

# Function to create a new access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()  # Copy the data to encode
    if expires_delta:
        expire = datetime.utcnow() + expires_delta  # Set expiration time
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Default expiration time is 15 minutes
    to_encode.update({"exp": expire})  # Add expiration to the payload
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Encode the JWT
    return encoded_jwt  # Return the encoded JWT
