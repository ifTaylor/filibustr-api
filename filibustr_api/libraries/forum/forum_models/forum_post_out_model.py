from pydantic import BaseModel
from datetime import datetime


class ForumPostOutModel(BaseModel):
    id: int
    thread_id: int
    content: str
    author_id: int
    created_at: datetime

    class Config:
        orm_mode = True
