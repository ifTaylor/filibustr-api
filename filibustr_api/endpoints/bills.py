from fastapi import APIRouter, Query, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Bill
from ..services.congress_api import CongressAPIClient
from ..services.bill_service import save_bill
from ..services.bill_service import get_bills_from_db
from ..database.database import DatabaseManager

router = APIRouter()

@router.get("/", response_model=List[Bill])
async def fetch_bills(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(DatabaseManager.get_session),
):
    # 1. Pull from DB first
    db_bills = await get_bills_from_db(session, limit=limit, offset=offset)

    # 2. If not enough bills exist, fetch from API and store
    if len(db_bills) < limit:
        client = CongressAPIClient()
        new_bills = client.get_active_bills(limit=limit, offset=offset)

        for bill in new_bills:
            await save_bill(session, bill)

        # Re-fetch after insertion
        db_bills = await get_bills_from_db(session, limit=limit, offset=offset)

    return db_bills
