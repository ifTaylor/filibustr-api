from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from filibustr_api.libraries.orm_base import Base


class ForumPostORM(Base):
    __tablename__ = "forum_posts"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    thread_id = Column(Integer, ForeignKey("forum_threads.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    thread = relationship("ForumThreadORM", back_populates="posts")
    author = relationship("UserORM", back_populates="posts")
