from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class HotelBookingStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"
    COMPLETED = "COMPLETED"

class RoomType(str, Enum):
    SINGLE = "SINGLE"
    DOUBLE = "DOUBLE"
    TWIN = "TWIN"
    TRIPLE = "TRIPLE"
    QUAD = "QUAD"
    KING = "KING"
    QUEEN = "QUEEN"
    SUITE = "SUITE"
    DELUXE = "DELUXE"
    EXECUTIVE = "EXECUTIVE"
    FAMILY = "FAMILY"

class GuestDetails(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    special_requests: Optional[str] = None

class RoomDetails(BaseModel):
    room_type: RoomType
    bed_type: Optional[str] = None
    room_description: Optional[str] = None
    price_per_night: float
    quantity: int = 1
    is_refundable: bool = False
    refund_policy: Optional[str] = None
    amenities: Optional[List[str]] = None
    view: Optional[str] = None
    max_occupancy: int = 2

class HotelPriceDetails(BaseModel):
    room_charges: float
    taxes: float
    fees: float
    total_price: float
    currency: str = "USD"
    price_breakdown: Optional[Dict[str, Any]] = None

class HotelLocation(BaseModel):
    address: str
    city: str
    state: Optional[str] = None
    country: str
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class HotelBase(BaseModel):
    booking_reference: Optional[str] = None
    user_id: Optional[str] = None
    hotel_id: str
    hotel_name: str
    hotel_chain: Optional[str] = None
    location: HotelLocation
    check_in: datetime
    check_out: datetime
    guests: List[GuestDetails]
    rooms: List[RoomDetails]
    price: HotelPriceDetails
    booking_date: Optional[datetime] = None
    status: HotelBookingStatus = HotelBookingStatus.PENDING
    star_rating: Optional[float] = None
    amenities: Optional[List[str]] = None
    images: Optional[List[str]] = None
    cancellation_deadline: Optional[datetime] = None

class HotelCreate(HotelBase):
    pass

class HotelUpdate(BaseModel):
    booking_reference: Optional[str] = None
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    guests: Optional[List[GuestDetails]] = None
    rooms: Optional[List[RoomDetails]] = None
    price: Optional[HotelPriceDetails] = None
    status: Optional[HotelBookingStatus] = None

class HotelInDBBase(HotelBase):
    hotel_booking_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Hotel(HotelInDBBase):
    pass

class HotelInDB(HotelInDBBase):
    pass

# Schema for hotel search parameters
class HotelSearchParams(BaseModel):
    city_code: str = Field(..., description="City code (e.g., 'NYC')")
    check_in_date: str = Field(..., description="Check-in date (YYYY-MM-DD)")
    check_out_date: str = Field(..., description="Check-out date (YYYY-MM-DD)")
    adults: int = Field(1, description="Number of adults")
    children: int = Field(0, description="Number of children")
    rooms: int = Field(1, description="Number of rooms")
    star_rating: Optional[int] = Field(None, description="Minimum star rating (1-5)")
    amenities: Optional[List[str]] = Field(None, description="Required amenities")
    radius: int = Field(5, description="Search radius")
    radius_unit: str = Field("KM", description="Radius unit (KM, MILE)")
    currency: str = Field("USD", description="Currency for pricing")
    max_price: Optional[float] = Field(None, description="Maximum price per night")