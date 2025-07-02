from pydantic import BaseModel
from typing import Optional
from .sponsor_model import Sponsor
from filibustr_api.database.bill_orm import BillORM


class Bill(BaseModel):
    number: int
    display_number: str
    title: str
    introduced_date: str
    congress: int
    bill_type: str
    current_chamber: Optional[str]
    current_status: Optional[str]
    sponsor: Sponsor

    @classmethod
    def from_api(cls, item: dict) -> "Bill":
        sponsor = Sponsor.from_api(
            sponsor_data=item.get("sponsor") or {},
            sponsor_role=item.get("sponsor_role") or {},
        )

        return cls(
            number=item["number"],
            display_number=item["display_number"],
            title=item["title"],
            introduced_date=item["introduced_date"],
            congress=item["congress"],
            bill_type=item["bill_type"],
            current_chamber=item.get("current_chamber"),
            current_status=item.get("current_status"),
            sponsor=sponsor,
        )

    @classmethod
    def from_orm_model(cls, orm_bill: "BillORM") -> "Bill":
        return cls(
            number=orm_bill.number,
            display_number=orm_bill.display_number,
            title=orm_bill.title,
            introduced_date=orm_bill.introduced_date.isoformat(),
            congress=orm_bill.congress,
            bill_type=orm_bill.bill_type,
            current_chamber=orm_bill.current_chamber,
            current_status=orm_bill.current_status,
            sponsor=Sponsor(
                name=orm_bill.sponsor_name or "",
                party=orm_bill.sponsor_party or "",
                state=orm_bill.sponsor_state or "",
                firstname="",
                lastname=""
            )
        )
