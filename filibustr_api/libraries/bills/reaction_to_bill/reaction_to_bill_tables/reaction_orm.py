from sqlalchemy import Column, String, Integer, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
import enum
import datetime

from filibustr_api.libraries.orm_base import Base


class ReactionEnum(str, enum.Enum):
    support = "support"
    oppose = "oppose"
    unsure = "unsure"
    outrage = "outrage"
    boring = "boring"


class BillReactionORM(Base):
    __tablename__ = "bill_reactions"

    id = Column(UUID(as_uuid=True), primary_key=True)
    bill_id = Column(Integer, index=True, nullable=False)
    user_id = Column(String, index=True, nullable=False)
    reaction = Column(Enum(ReactionEnum), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
