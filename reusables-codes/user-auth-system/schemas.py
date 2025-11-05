from pydantic import BaseModel, EmailStr
from datetime import datetime, timezone

class UserBase(BaseModel):
    username: str
    email: EmailStr
    phone_number: str | None = None # Optional
    full_name: str | None = None # Optional
    is_active: bool = True # Active by default
    is_admin: bool = False
    is_verified: bool = False

class UserCreate(UserBase):
    password: str 

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

   

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None # Optional
    full_name: str | None = None # Optional
    is_active: bool | None = None 
    is_admin: bool | None = None
    is_verified: bool | None = None
    updated_at: datetime = datetime.now(timezone.utc)
    
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenData(BaseModel):
    access_token: str
    token_type: str

