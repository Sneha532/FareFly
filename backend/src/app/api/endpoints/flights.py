from typing import Any, List, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src.app import crud
from src.app import schemas
from src.app.api import deps
from src.app.services.amadeus import amadeus_service

router = APIRouter()

@router.post("/search", response_model=List[Dict[str, Any]])
async def search_flights(
    *,
    origin: str = Query(..., description="Origin airport code (e.g., 'JFK')"),
    destination: str = Query(..., description="Destination airport code (e.g., 'CDG')"),
    departure_date: str = Query(..., description="Departure date (YYYY-MM-DD)"),
    return_date: Optional[str] = Query(None, description="Return date (YYYY-MM-DD) for round trips"),
    adults: int = Query(1, description="Number of adult passengers"),
    travel_class: str = Query("ECONOMY", description="Travel class (ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST)"),
) -> Any:
    """
    Search for flights using Amadeus API
    """
    flights = await amadeus_service.search_flights(
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        return_date=return_date,
        adults=adults,
        travel_class=travel_class
    )
    return flights

@router.post("/{itinerary_id}/add", response_model=schemas.Itinerary)
def add_flight_to_itinerary(
    *,
    db: Session = Depends(deps.get_db),
    itinerary_id: str,
    flight_data: Dict[str, Any],
    current_user = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add a flight to an itinerary
    """
    itinerary = crud.itinerary.get(db=db, id=itinerary_id)
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    
    if itinerary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    updated_itinerary = crud.itinerary.add_flight(
        db=db, itinerary_id=itinerary_id, flight_data=flight_data
    )
    return updated_itinerary