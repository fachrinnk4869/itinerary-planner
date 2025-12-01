from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date as dt
from datetime import time


class Activity(BaseModel):
    time: str = Field(description="Time of the activity in HH:MM format")
    title: str
    details: str


class Days(BaseModel):
    date: dt = Field(description="Date of the day in YYYY-MM-DD format")
    city: str
    activities: List[Activity]


class Plan(BaseModel):
    start_date: dt = Field(
        description="Start date of the trip in YYYY-MM-DD format")
    end_date: dt = Field(
        description="End date of the trip in YYYY-MM-DD format")
    days: List[Days]
