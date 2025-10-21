from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    # id: int
    email: EmailStr
    password: str
    # phone_number:

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: int | None = None # Optional[int] = None

class PostCreate(PostBase):
    # inherit all props from parent
    pass

class PostResponse(PostBase):
    # will get these fields only
    id: int
    owner_id: int
    created_at: datetime
    owner: UserResponse

    # convert the model resp to a dict
    class Config:
        orm_mode = True 



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    