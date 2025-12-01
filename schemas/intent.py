from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date


class Intent(BaseModel):
    """
    Represents the user's travel intent extracted from their input.
    """
    destination: Optional[str]
    start_date: Optional[date] = Field(
        description=f"Start date of the trip look at format YYYY-MM-DD look at time right now in UTC plus user start date. Right now is {datetime.now()}")
    end_date: Optional[date] = Field(
        description="Start date of the trip look at format YYYY-MM-DD")
    budget_range: Optional[str] = Field(
        description="Average budget range for the trip in Rupiah")
    notes: Optional[str]
