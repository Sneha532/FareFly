from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class FlightClass(str, Enum):
    ECONOMY = "ECONOMY"
    PREMIUM_ECONOMY = "PREMIUM_ECONOMY"
    BUSINESS = "BUSINESS"
    FIRST = "FIRST"

class FlightStatus(str, Enum):
    SCHEDULED = "SCHEDULED"
    DELAYED = "DELAYED"
    BOARDING = "BOARDING"
    ON_TIME = "ON_TIME"
    DEPARTED = "DEPARTED"
    ARRIVED = "ARRIVED"
    CANCELLED = "CANCELLED"

class BookingStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"
    COMPLETED = "COMPLETED"

class PassengerDetails(BaseModel):
    first_name: str
    last_name: str
    passport_number: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    nationality: Optional[str] = None
    seat_number: Optional[str] = None

class FlightSegment(BaseModel):
    departure_airport: str
    arrival_airport: str
    departure_time: datetime
    arrival_time: datetime
    flight_number: str
    carrier: str
    duration: Optional[str] = None
    aircraft: Optional[str] = None
    stops: int = 0
    terminal_departure: Optional[str] = None
    terminal_arrival: Optional[str] = None
    cabin_class: FlightClass
    status: FlightStatus = FlightStatus.SCHEDULED

class PriceDetails(BaseModel):
    base_fare: float
    taxes: float
    fees: float
    total_price: float
    currency: str = "USD"
    refundable: bool = False

class FlightBase(BaseModel):
    booking_reference: Optional[str] = None
    user_id: Optional[str] = None
    segments: List[FlightSegment]
    passengers: List[PassengerDetails]
    price: PriceDetails
    booking_date: Optional[datetime] = None
    status: BookingStatus = BookingStatus.PENDING
    is_round_trip: bool = False

class FlightCreate(FlightBase):
    booking_reference: Optional[str] = None
    user_id: Optional[str] = None
    booking_date: Optional[datetime] = None
    

class FlightUpdate(BaseModel):
    booking_reference: Optional[str] = None
    segments: Optional[List[FlightSegment]] = None
    passengers: Optional[List[PassengerDetails]] = None
    price: Optional[PriceDetails] = None
    status: Optional[BookingStatus] = None

class FlightInDBBase(FlightBase):
    booking_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Flight(FlightInDBBase):
    pass

class FlightInDB(FlightInDBBase):
    pass

# Schema for flight search parameters
class FlightSearchParams(BaseModel):
    origin: str = Field(..., description="Origin airport code (e.g., 'JFK')")
    destination: str = Field(..., description="Destination airport code (e.g., 'CDG')")
    departure_date: str = Field(..., description="Departure date (YYYY-MM-DD)")
    return_date: Optional[str] = Field(None, description="Return date (YYYY-MM-DD) for round trips")
    adults: int = Field(1, description="Number of adult passengers")
    children: int = Field(0, description="Number of child passengers")
    infants: int = Field(0, description="Number of infant passengers")
    travel_class: FlightClass = Field(FlightClass.ECONOMY, description="Travel class")
    non_stop: bool = Field(False, description="Only show non-stop flights")
    currency: str = Field("USD", description="Currency for pricing")
    max_price: Optional[float] = Field(None, description="Maximum price")