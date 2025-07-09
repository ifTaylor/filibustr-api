from pydantic import BaseModel
from typing import Optional, Literal

from filibustr_api.libraries.bills.reaction_to_bill.reaction_to_bill_models.bill_reaction_counts_model import (
    BillReactionCounts,
)
from filibustr_api.libraries.bills.active_bill.active_bill_models.sponsor_model import (
    Sponsor,
)
from filibustr_api.libraries.bills.active_bill.active_bill_tables.bill_orm import (
    BillORM,
)


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

    reactions: Optional[BillReactionCounts] = None
    user_reaction: Optional[
        Literal["support", "oppose", "unsure", "outrage", "boring"]
    ] = None

    @classmethod
    def from_api(cls, item: dict, reactions=None, user_reaction=None) -> "Bill":
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
            reactions=BillReactionCounts(**reactions) if reactions else None,
            user_reaction=user_reaction,
        )

    @classmethod
    def from_orm_model(
        cls, orm_bill: BillORM, reactions=None, user_reaction=None
    ) -> "Bill":
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
                lastname="",
            ),
            reactions=BillReactionCounts(**reactions) if reactions else None,
            user_reaction=user_reaction,
        )
