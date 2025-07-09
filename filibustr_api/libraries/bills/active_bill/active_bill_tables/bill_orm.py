from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from filibustr_api.libraries.orm_base import Base


class BillORM(Base):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer)
    display_number = Column(String)
    title = Column(String)
    introduced_date = Column(Date)
    congress = Column(Integer)
    bill_type = Column(String)
    current_chamber = Column(String)
    current_status = Column(String)

    sponsor_id = Column(Integer, ForeignKey("sponsors.id"))
    sponsor = relationship("SponsorORM", back_populates="bills")
