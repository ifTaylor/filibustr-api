from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from filibustr_api.libraries.orm_base import Base


class UserORM(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Integer, default=1)

    preferences = relationship(
        "UserPreferencesORM",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )