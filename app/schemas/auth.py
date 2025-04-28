from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None
    exp: Optional[datetime] = None

class UserBase(BaseModel):
    email: str
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: int
    hashed_password: str

    class Config:
        from_attributes = True 