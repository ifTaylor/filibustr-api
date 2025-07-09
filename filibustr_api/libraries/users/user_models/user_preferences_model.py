from pydantic import BaseModel
from typing import Optional, Dict


class UserPreferencesModel(BaseModel):
    theme: Optional[str] = "light"
    language: Optional[str] = "en"
    notifications_enabled: Optional[int] = 1
    advanced: Optional[Dict] = {}

    class Config:
        orm_mode = True
