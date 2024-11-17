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