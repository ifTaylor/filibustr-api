from pydantic import BaseModel
from datetime import datetime

class ForumPostCreateModel(BaseModel):
    thread_id: int
    content: str
