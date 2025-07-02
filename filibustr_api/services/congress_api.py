from typing import List
import requests
from pydantic import ValidationError

from ..models.bill_model import Bill


class CongressAPIClient:
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
            raise Exception(f"Failed to fetch bills: {response.status_code} {response.text}")

        bill_items = response.json().get("objects", [])
        bills: List[Bill] = []

        for item in bill_items:
            try:
                bill = Bill.from_api(item)
                bills.append(bill)
            except (KeyError, ValidationError) as e:
                print(f"Skipping bill due to error: {e}")

        return bills
