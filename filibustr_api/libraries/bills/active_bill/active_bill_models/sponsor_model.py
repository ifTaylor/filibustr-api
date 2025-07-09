from typing import Optional

from pydantic import BaseModel


class Sponsor(BaseModel):
    name: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    party: Optional[str] = None
    state: Optional[str] = None

    @classmethod
    def from_api(cls, sponsor_data: dict, sponsor_role: dict) -> "Sponsor":
        return cls(
            firstname=sponsor_data.get("firstname", ""),
            lastname=sponsor_data.get("lastname", ""),
            name=sponsor_data.get("name", ""),
            party=sponsor_role.get("party", "Unknown"),
            state=sponsor_role.get("state", "Unknown"),
        )
