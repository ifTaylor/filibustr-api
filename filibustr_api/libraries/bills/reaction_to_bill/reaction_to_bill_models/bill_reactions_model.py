from datetime import datetime
from typing import Optional, Literal
from uuid import UUID

from pydantic import BaseModel


class BillReaction(BaseModel):
    id: UUID
    bill_id: int
    user_id: Optional[str]  # anonymous or UUID
    reaction: Literal["support", "oppose", "unsure", "outrage", "boring"]
    created_at: datetime
