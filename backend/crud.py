from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from typing import Optional
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import schemas, database, models
from fastapi import APIRouter, Depends, status, HTTPException
#from ..hashing import Hash


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    return db.query(models.User).filter(models.User.username==username).first()
    
def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_user(request:schemas.UserCreate, db: Session):
    new_user = models.User(username=request.username, email=request.email, hashed_password=get_password_hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all(db: Session):
    users = db.query(models.User).all()
    return users

def update(id, request: schemas.UserCreate, db: Session):
    users = db.query(models.User).filter(models.User.id == id)
    if not users.first():
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND, detail = f"Blog with id {id} not found")
    users.update({'username':request.username, 'email':request.email})
    db.commit()
    return "updated"

