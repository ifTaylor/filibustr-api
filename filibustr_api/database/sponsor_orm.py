from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class SponsorORM(Base):
    __tablename__ = "sponsors"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    name = Column(String)
    party = Column(String)
    state = Column(String)

    bills = relationship("BillORM", back_populates="sponsor")
