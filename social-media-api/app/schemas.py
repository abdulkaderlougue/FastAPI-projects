from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: int | None = None # Optional[int] = None


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str
    # phone_number: