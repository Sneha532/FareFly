from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

# Flight schema
class Flight(BaseModel):
    carrier: str
    flight_number: str
    departure_airport: str
    arrival_airport: str
    departure_time: datetime
    arrival_time: datetime
    price: float
    currency: str
    cabin_class: str

# Hotel schema
class Hotel(BaseModel):
    name: str
    address: str
    city: str
    check_in: datetime
    check_out: datetime
    price: float
    currency: str
    room_type: str
    amenities: List[str]

# Attraction schema
class Attraction(BaseModel):
    name: str
    location: str
    visit_date: datetime
    category: str
    description: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None

# Shared properties
class ItineraryBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    is_public: bool = False

# Properties to receive via API on creation
class ItineraryCreate(ItineraryBase):
    flights: Optional[List[Dict[str, Any]]] = []
    hotels: Optional[List[Dict[str, Any]]] = []
    attractions: Optional[List[Dict[str, Any]]] = []

# Properties to receive via API on update
class ItineraryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_public: Optional[bool] = None
    flights: Optional[List[Dict[str, Any]]] = None
    hotels: Optional[List[Dict[str, Any]]] = None
    attractions: Optional[List[Dict[str, Any]]] = None

# Properties shared by models stored in DB
class ItineraryInDBBase(ItineraryBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    flights: List[Dict[str, Any]] = []
    hotels: List[Dict[str, Any]] = []
    attractions: List[Dict[str, Any]] = []

    class Config:
        orm_mode = True

# Properties to return via API
class Itinerary(ItineraryInDBBase):
    pass

# Properties stored in DB
class ItineraryInDB(ItineraryInDBBase):
    pass