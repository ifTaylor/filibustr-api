from pydantic import BaseModel
from datetime import datetime


class ForumThreadCreateModel(BaseModel):
    title: str
