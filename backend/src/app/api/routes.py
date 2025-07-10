from fastapi import APIRouter

from src.app.api.endpoints import itineraries, flights, hotels, attractions, auth

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(itineraries.router, prefix="/itineraries", tags=["itineraries"])
api_router.include_router(flights.router, prefix="/flights", tags=["flights"])
api_router.include_router(hotels.router, prefix="/hotels", tags=["hotels"])
api_router.include_router(attractions.router, prefix="/attractions", tags=["attractions"])