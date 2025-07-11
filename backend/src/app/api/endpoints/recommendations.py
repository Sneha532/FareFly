from typing import Any, List, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.app.api import deps
from src.app.services.gemini import gemini_service
from src.app.services.unsplash import unsplash_service

router = APIRouter()

@router.get("/tourist-places", response_model=List[Dict[str, Any]])
async def get_tourist_places(
    destination: str,
    interests: Optional[List[str]] = Query(None),
    duration_days: Optional[int] = Query(3, ge=1, le=30),
    budget: Optional[str] = Query("medium", regex="^(low|medium|high)$"),
    # Remove the authentication dependency for testing
    # current_user = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get recommendations for tourist places based on destination and preferences.
    """
    recommendations = await gemini_service.get_place_recommendations(
        destination=destination,
        interests=interests,
        duration_days=duration_days,
        budget=budget
    )
    
    if not recommendations:
        raise HTTPException(
            status_code=404,
            detail=f"Could not find recommendations for {destination}"
        )
    
    # Add Unsplash image for each recommendation
    for rec in recommendations:
        # Create a search query based on the attraction name and destination
        search_query = f"{rec['name']} {destination}"
        
        # Use the Unsplash API service to get an image
        photo = await unsplash_service.search_photo(search_query)
        
        if photo:
            # Add image URLs of different sizes
            rec["image_url"] = photo["urls"]["regular"]
            rec["image_thumb"] = photo["urls"]["thumb"]
            rec["image_author"] = photo["user"]["name"]
            rec["image_attribution_url"] = photo["links"]["html"]
        else:
            # Fallback to a random destination photo
            random_photo = await unsplash_service.get_random_photo(destination)
            if random_photo:
                rec["image_url"] = random_photo["urls"]["regular"]
                rec["image_thumb"] = random_photo["urls"]["thumb"]
                rec["image_author"] = random_photo["user"]["name"]
                rec["image_attribution_url"] = random_photo["links"]["html"]
            else:
                # Last resort fallback - placeholder
                rec["image_url"] = "https://placehold.co/600x400/007bff/white?text=No+Image+Found"
                rec["image_thumb"] = "https://placehold.co/200x200/007bff/white?text=No+Image"
                rec["image_author"] = "None"
                rec["image_attribution_url"] = ""
    
    return recommendations
