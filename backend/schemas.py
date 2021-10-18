from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None

    class Config:
	    orm_mode=True

class UserInDB(User):
    hashed_password: str

class UserCreate(User):
    password: str
