from pydantic import BaseModel, EmailStr, Field 
from typing import Optional, Any
from datetime import datetime

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

# Properties to receive via API on creation
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None

# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    # Change from 'use_idid' to 'id'
    id: str  # This field matches what you return in the /me endpoint
    email: EmailStr
    full_name: Optional[str]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes= True
# Additional properties to return via API
class User(UserInDBBase):
    """
    User schema to return to client
    """
    class Config:
       from_attributes= True
# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str

class Token(BaseModel):
    """Schema for the token response."""
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    """Schema for the token payload."""
    sub: Optional[Any] = None
    exp: Optional[int] = None

    # models.py or schemas.py


class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
