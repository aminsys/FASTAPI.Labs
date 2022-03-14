from pydantic import BaseModel, EmailStr
from datetime import datetime
# Defning what a post should look like. Getting validation for free.
# This way we can guarantee that the front end will send the type of data that we want.
# The structure of the request/ response.

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class UserCreate(BaseModel):
    email: EmailStr # Validate that this is valid email and not some random string
    password: str


class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    created_at: datetime

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True