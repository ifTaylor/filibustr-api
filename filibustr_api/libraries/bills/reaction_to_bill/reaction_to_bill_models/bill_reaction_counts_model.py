from pydantic import BaseModel


class BillReactionCounts(BaseModel):
    support: int = 0
    oppose: int = 0
    unsure: int = 0
    outrage: int = 0
    boring: int = 0
