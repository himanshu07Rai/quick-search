from sqlmodel import SQLModel, Field
import uuid
from typing import Optional
from datetime import datetime

class Post(SQLModel, table=True):
    __tablename__ = "posts"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    title: str
    content: str
    likes: Optional[int] = Field(default=0)
    comments: Optional[int] = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.now)
    def __repr__(self):
        return f"Post {self.id}: {self.title}"