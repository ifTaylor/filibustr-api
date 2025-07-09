from pydantic import BaseModel
from datetime import datetime


class ForumThreadOutModel(BaseModel):
    id: int
    title: str
    creator_id: int
    created_at: datetime

    class Config:
        orm_mode = True
