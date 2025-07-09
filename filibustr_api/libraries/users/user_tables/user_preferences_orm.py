from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship

from filibustr_api.libraries.orm_base import Base


class UserPreferencesORM(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    theme = Column(String, default="light")
    language = Column(String, default="en")
    notifications_enabled = Column(Integer, default=1)
    advanced = Column(JSON, nullable=True)

    user = relationship("UserORM", back_populates="preferences")
