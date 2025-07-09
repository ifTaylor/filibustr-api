from typing import List
import requests
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from filibustr_api.libraries.bills.active_bill.active_bill_models.bill_model import (
    Bill,
    Sponsor,
)
from filibustr_api.libraries.bills.active_bill.active_bill_tables.bill_orm import (
    BillORM,
)
from filibustr_api.libraries.bills.active_bill.active_bill_tables.sponsor_orm import (
    SponsorORM,
)
from sqlalchemy.orm import selectinload

from filibustr_api.libraries.bills.active_bill.active_bill_models.bill_model import Bill


class ActiveBill:
    BASE_URL = "https://www.govtrack.us/api/v2"

    def __init__(self, congress: int = 118):
        self.congress = congress

    def get_active_bills(self, limit: int = 20, offset: int = 0) -> List[Bill]:
        url = (
            f"{self.BASE_URL}/bill?"
            f"congress={self.congress}&sort=-introduced_date"
            f"&limit={limit}&offset={offset}"
        )
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch bills: {response.status_code} {response.text}"
            )

        bill_items = response.json().get("objects", [])
        bills: List[Bill] = []

        for item in bill_items:
            try:
                bill = Bill.from_api(item)
                bills.append(bill)
            except (KeyError, ValidationError) as e:
                print(f"Skipping bill due to error: {e}")

        return bills

    async def get_bills_from_db(
        self, session: AsyncSession, limit: int, offset: int
    ) -> list[Bill]:
        stmt = (
            select(BillORM)
            .options(selectinload(BillORM.sponsor))  # Eager-load sponsor
            .offset(offset)
            .limit(limit)
        )
        result = await session.execute(stmt)
        records = result.scalars().all()

        return [
            Bill(
                number=r.number,
                display_number=r.display_number,
                title=r.title,
                introduced_date=r.introduced_date.isoformat(),
                congress=r.congress,
                bill_type=r.bill_type,
                current_chamber=r.current_chamber,
                current_status=r.current_status,
                sponsor=(
                    Sponsor(
                        name=r.sponsor.name,
                        firstname=r.sponsor.firstname,
                        lastname=r.sponsor.lastname,
                        party=r.sponsor.party,
                        state=r.sponsor.state,
                    )
                    if r.sponsor
                    else None
                ),
            )
            for r in records
        ]

    async def save_bill(self, session: AsyncSession, bill: Bill) -> None:
        # Check if bill already exists
        exists = await session.execute(
            select(BillORM).where(BillORM.number == bill.number)
        )
        if exists.scalars().first():
            return

        # Check if sponsor already exists
        sponsor_result = await session.execute(
            select(SponsorORM).where(SponsorORM.name == bill.sponsor.name)
        )
        db_sponsor = sponsor_result.scalars().first()

        # If sponsor doesn't exist, create it
        if not db_sponsor:
            db_sponsor = SponsorORM(
                firstname=bill.sponsor.firstname,
                lastname=bill.sponsor.lastname,
                name=bill.sponsor.name,
                party=bill.sponsor.party,
                state=bill.sponsor.state,
            )
            session.add(db_sponsor)
            await session.flush()  # ensures sponsor.id is available

        # Create new bill and link to sponsor
        db_bill = BillORM(
            number=bill.number,
            display_number=bill.display_number,
            title=bill.title,
            introduced_date=date.fromisoformat(bill.introduced_date),
            congress=bill.congress,
            bill_type=bill.bill_type,
            current_chamber=bill.current_chamber,
            current_status=bill.current_status,
            sponsor=db_sponsor,
        )
        session.add(db_bill)
        await session.commit()
