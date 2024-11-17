from pydantic import BaseModel
import uuid
from datetime import datetime

class PostCreateSchema(BaseModel):
    title: str
    content: str

class PostSchema(PostCreateSchema):
    id: uuid.UUID
    title: str 
    content: str
    likes: int
    comments: int
    created_at: datetime
    class Config:
        # Add from_attributes=True to enable ORM compatibility with Pydantic
        from_attributes = True