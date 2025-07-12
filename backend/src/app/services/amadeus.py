from amadeus import Client, ResponseError
from src.app.core.config import settings
from fastapi import HTTPException
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class AmadeusService:
    def __init__(self):
        self.amadeus = Client(
            client_id=settings.AMADEUS_CLIENT_ID,
            client_secret=settings.AMADEUS_CLIENT_SECRET
        )
    
    async def search_flights(self, 
                            origin: str, 
                            destination: str, 
                            departure_date: str, 
                            return_date: Optional[str] = None,
                            adults: int = 1,
                            travel_class: str = "ECONOMY",
                            max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search for flights using Amadeus Flight Offers Search API
        """
        try:
            if return_date:
                response = self.amadeus.shopping.flight_offers_search.get(
                    originLocationCode=origin,
                    destinationLocationCode=destination,
                    departureDate=departure_date,
                    returnDate=return_date,
                    adults=adults,
                    travelClass=travel_class,
                    max=max_results
                )
            else:
                response = self.amadeus.shopping.flight_offers_search.get(
                    originLocationCode=origin,
                    destinationLocationCode=destination,
                    departureDate=departure_date,
                    adults=adults,
                    travelClass=travel_class,
                    max=max_results
                )
                
            return response.data
            
        except ResponseError as error:
            logger.error(f"Amadeus API Error: {error}")
            raise HTTPException(
                status_code=error.response.status_code,
                detail=error.response.result.get('errors', [{'detail': 'Unknown error'}])[0].get('detail')
            )
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred: {str(e)}"
            )
    
    async def search_hotels(self,
                           city_code: str,
                           check_in_date: str,
                           check_out_date: str,
                           adults: int = 1,
                           radius: int = 5,
                           radius_unit: str = "KM") -> List[Dict[str, Any]]:
        """
        Search for hotels using Amadeus Hotel Search API
        """
        try:
            response = await self.amadeus.shopping.hotel_offers.get(
                cityCode=city_code,
                checkInDate=check_in_date,
                checkOutDate=check_out_date,
                adults=adults,
                radius=radius,
                radiusUnit=radius_unit
            )
            return response.data
        except Exception as e:
            logger.error(f"Error searching hotels: {e}")
            # If Amadeus API fails, return sample data for development
            return self._get_sample_hotel_data(city_code)
        
    def _get_sample_hotel_data(self, city_code):
        """Return sample hotel data for development purposes"""
        return [
            {
                "name": "Grand Hotel Plaza",
                "rating": 4.5,
                "address": {
                    "lines": [f"{city_code} Downtown, Main Street 123"]
                },
                "price": {
                    "total": "129.99",
                    "currency": "USD"
                }
            },
            {
                "name": "Skyline Suites",
                "rating": 4.0,
                "address": {
                    "lines": [f"{city_code} Business District, Tower Road 45"]
                },
                "price": {
                    "total": "159.99",
                    "currency": "USD"
                }
            },
            {
                "name": "Comfort Inn Express",
                "rating": 3.5,
                "address": {
                    "lines": [f"{city_code} Airport Area, Terminal Blvd 78"]
                },
                "price": {
                    "total": "89.99",
                    "currency": "USD"
                }
            },
            {
                "name": "Riverside Resort",
                "rating": 4.2,
                "address": {
                    "lines": [f"{city_code} Waterfront, Harbor Street 212"]
                },
                "price": {
                    "total": "179.99",
                    "currency": "USD"
                }
            }
        ]
    
    async def search_points_of_interest(self,
                                      latitude: float,
                                      longitude: float,
                                      radius: int = 5,
                                      categories: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Search for points of interest using Amadeus Points of Interest API
        """
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "radius": radius
            }
            
            if categories:
                params["categories"] = ",".join(categories)
                
            response = self.amadeus.reference_data.locations.points_of_interest.get(**params)
            return response.data
            
        except ResponseError as error:
            logger.error(f"Amadeus API Error: {error}")
            raise HTTPException(
                status_code=error.response.status_code,
                detail=error.response.result.get('errors', [{'detail': 'Unknown error'}])[0].get('detail')
            )
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred: {str(e)}"
            )

# Create a singleton instance
amadeus_service = AmadeusService()