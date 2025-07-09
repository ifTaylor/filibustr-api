from fastapi import APIRouter, Query, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from ..libraries.bills.active_bill.active_bill_models import Bill
from filibustr_api.libraries.bills.active_bill.active_bill import ActiveBill
from ..database import DatabaseManager

router = APIRouter()


@router.get("/", response_model=List[Bill])
async def fetch_bills(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(DatabaseManager.get_session),
):
    active_bill = ActiveBill()
    # 1. Pull from DB first
    db_bills = await active_bill.get_bills_from_db(session, limit=limit, offset=offset)

    # 2. If not enough bills exist, fetch from API and store
    if len(db_bills) < limit:
        new_bills = active_bill.get_active_bills(limit=limit, offset=offset)

        for bill in new_bills:
            await active_bill.save_bill(session, bill)

        # Re-fetch after insertion
        db_bills = await active_bill.get_bills_from_db(
            session, limit=limit, offset=offset
        )

    return db_bills
