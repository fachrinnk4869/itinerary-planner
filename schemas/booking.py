from pydantic import BaseModel, Field
from typing import List, Optional


class FlightBooking(BaseModel):
    provider: str = Field(description="Flight provider or agency name")
    booking_reference: str = Field(
        description="Booking reference number for the flight")


class HotelBooking(BaseModel):
    hotel_name: str = Field(description="Name of the hotel")
    booking_reference: str = Field(
        description="Booking reference number for the hotel")


class Booking(BaseModel):
    flights: List[FlightBooking] = Field(
        description="List of booked flight provider, agencies, and booking reference numbers")
    hotels: List[HotelBooking] = Field(
        description="List of booked hotels and their booking reference numbers")
