from pydantic import BaseModel
from datetime import datetime

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
    created_at: datetime

    # convert the model resp to a dict
    class Config:
        orm_mode = True 

class User(BaseModel):
    id: int
    name: str
    email: str
    password: str
    # phone_number: