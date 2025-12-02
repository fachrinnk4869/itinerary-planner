from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from fastapi import Query


class itineraryQuery(BaseModel):
    input: str = Query(
        default="Plan a romantic 4-day trip to Bali next month. Booking OK.",
        min_length=1,
        description="User input for itinerary planning")
    auto_book: bool = Query(
        default=False, description="Whether to auto book the trip or not")


class FinalTripPlan(BaseModel):
    trip_title: str
    start_date: date
    end_date: date
    itinerary: list
    flights: list
    hotels: list
    notes: str | None = None
    payment: dict | None = None
