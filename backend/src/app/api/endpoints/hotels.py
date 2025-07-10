from typing import Any, List, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.app import schemas, crud  # Fixed import
from src.app.api import deps  # Fixed import
from src.app.services.amadeus import amadeus_service  # Fixed import

router = APIRouter()

@router.post("/search", response_model=List[Dict[str, Any]])
async def search_hotels(
    *,
    city_code: str = Query(..., description="City code (e.g., 'NYC')"),
    check_in_date: str = Query(..., description="Check-in date (YYYY-MM-DD)"),
    check_out_date: str = Query(..., description="Check-out date (YYYY-MM-DD)"),
    adults: int = Query(1, description="Number of adults"),
    radius: int = Query(5, description="Search radius"),
    radius_unit: str = Query("KM", description="Radius unit (KM, MILE)"),
    current_user = Depends(deps.get_current_active_user),
) -> Any:
    """
    Search for hotels using Amadeus API
    """
    hotels = await amadeus_service.search_hotels(
        city_code=city_code,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        adults=adults,
        radius=radius,
        radius_unit=radius_unit
    )
    return hotels

@router.post("/{itinerary_id}/add", response_model=schemas.Itinerary)
def add_hotel_to_itinerary(
    *,
    db: Session = Depends(deps.get_db),
    itinerary_id: str,
    hotel_data: Dict[str, Any],
    current_user = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add a hotel to an itinerary
    """
    itinerary = crud.itinerary.get(db=db, id=itinerary_id)
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    
    if itinerary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    updated_itinerary = crud.itinerary.add_hotel(
        db=db, itinerary_id=itinerary_id, hotel_data=hotel_data
    )
    return updated_itinerary