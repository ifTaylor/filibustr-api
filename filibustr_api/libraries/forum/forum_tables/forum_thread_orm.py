from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from filibustr_api.libraries.orm_base import Base


class ForumThreadORM(Base):
    __tablename__ = "forum_threads"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    creator = relationship("UserORM", back_populates="threads")
    posts = relationship("ForumPostORM", back_populates="thread", cascade="all, delete-orphan")
