from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.models.itinerary import Itinerary
from app.schemas.itinerary import ItineraryCreate, ItineraryUpdate

class CRUDItinerary(CRUDBase[Itinerary, ItineraryCreate, ItineraryUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: ItineraryCreate, user_id: str
    ) -> Itinerary:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Itinerary(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[Itinerary]:
        return (
            db.query(self.model)
            .filter(Itinerary.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_public(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Itinerary]:
        return (
            db.query(self.model)
            .filter(Itinerary.is_public == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def add_flight(
        self, db: Session, *, itinerary_id: str, flight_data: Dict[str, Any]
    ) -> Itinerary:
        itinerary = db.query(self.model).filter(Itinerary.id == itinerary_id).first()
        if not itinerary:
            return None
        
        if not itinerary.flights:
            itinerary.flights = []
            
        itinerary.flights.append(flight_data)
        db.add(itinerary)
        db.commit()
        db.refresh(itinerary)
        return itinerary
    
    def add_hotel(
        self, db: Session, *, itinerary_id: str, hotel_data: Dict[str, Any]
    ) -> Itinerary:
        itinerary = db.query(self.model).filter(Itinerary.id == itinerary_id).first()
        if not itinerary:
            return None
        
        if not itinerary.hotels:
            itinerary.hotels = []
            
        itinerary.hotels.append(hotel_data)
        db.add(itinerary)
        db.commit()
        db.refresh(itinerary)
        return itinerary
    
    def add_attraction(
        self, db: Session, *, itinerary_id: str, attraction_data: Dict[str, Any]
    ) -> Itinerary:
        itinerary = db.query(self.model).filter(Itinerary.id == itinerary_id).first()
        if not itinerary:
            return None
        
        if not itinerary.attractions:
            itinerary.attractions = []
            
        itinerary.attractions.append(attraction_data)
        db.add(itinerary)
        db.commit()
        db.refresh(itinerary)
        return itinerary

itinerary = CRUDItinerary(Itinerary)