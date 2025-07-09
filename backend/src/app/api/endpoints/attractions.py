from typing import Any, List, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api import deps
from app.services.amadeus import amadeus_service

router = APIRouter()

@router.get("/search", response_model=List[Dict[str, Any]])
async def search_attractions(
    *,
    latitude: float = Query(..., description="Latitude of the location"),
    longitude: float = Query(..., description="Longitude of the location"),
    radius: int = Query(5, description="Search radius in km"),
    categories: Optional[List[str]] = Query(None, description="Categories of attractions"),
    current_user = Depends(deps.get_current_active_user),
) -> Any:
    """
    Search for attractions using Amadeus API
    """
    attractions = await amadeus_service.search_points_of_interest(
        latitude=latitude,
        longitude=longitude,
        radius=radius,
        categories=categories
    )
    return attractions

@router.post("/{itinerary_id}/add", response_model=schemas.Itinerary)
def add_attraction_to_itinerary(
    *,
    db: Session = Depends(deps.get_db),
    itinerary_id: str,
    attraction_data: Dict[str, Any],
    current_user = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add an attraction to an itinerary
    """
    itinerary = crud.itinerary.get(db=db, id=itinerary_id)
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    
    if itinerary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    updated_itinerary = crud.itinerary.add_attraction(
        db=db, itinerary_id=itinerary_id, attraction_data=attraction_data
    )
    return updated_itinerary