from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Itinerary])
def read_itineraries(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve itineraries.
    """
    if crud.user.is_superuser(current_user):
        itineraries = crud.itinerary.get_multi(db, skip=skip, limit=limit)
    else:
        itineraries = crud.itinerary.get_multi_by_owner(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )
    return itineraries

@router.get("/public", response_model=List[schemas.Itinerary])
def read_public_itineraries(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve public itineraries.
    """
    itineraries = crud.itinerary.get_public(db, skip=skip, limit=limit)
    return itineraries

@router.post("/", response_model=schemas.Itinerary)
def create_itinerary(
    *,
    db: Session = Depends(deps.get_db),
    itinerary_in: schemas.ItineraryCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new itinerary.
    """
    itinerary = crud.itinerary.create_with_owner(
        db=db, obj_in=itinerary_in, user_id=current_user.id
    )
    return itinerary

@router.get("/{id}", response_model=schemas.Itinerary)
def read_itinerary(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get itinerary by ID.
    """
    itinerary = crud.itinerary.get(db=db, id=id)
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    if not crud.user.is_superuser(current_user) and (
        itinerary.user_id != current_user.id and not itinerary.is_public
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return itinerary

@router.put("/{id}", response_model=schemas.Itinerary)
def update_itinerary(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    itinerary_in: schemas.ItineraryUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an itinerary.
    """
    itinerary = crud.itinerary.get(db=db, id=id)
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    if not crud.user.is_superuser(current_user) and (itinerary.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    itinerary = crud.itinerary.update(db=db, db_obj=itinerary, obj_in=itinerary_in)
    return itinerary

@router.delete("/{id}", response_model=schemas.Itinerary)
def delete_itinerary(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an itinerary.
    """
    itinerary = crud.itinerary.get(db=db, id=id)
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    if not crud.user.is_superuser(current_user) and (itinerary.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    itinerary = crud.itinerary.remove(db=db, id=id)
    return itinerary