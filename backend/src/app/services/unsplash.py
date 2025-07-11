import httpx
from typing import Optional, Dict, Any
import logging

from src.app.core.config import settings

logger = logging.getLogger(__name__)

class UnsplashService:
    def __init__(self):
        self.access_key = settings.UNSPLASH_ACCESS_KEY
        self.base_url = "https://api.unsplash.com"
        self.headers = {"Authorization": f"Client-ID {self.access_key}"}
    
    async def search_photo(self, query: str) -> Optional[Dict[str, Any]]:
        """Search for a photo on Unsplash based on a query."""
        try:
            logger.info(f"Searching Unsplash for: {query}")
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/search/photos",
                    params={"query": query, "per_page": 1},
                    headers=self.headers
                )
                response.raise_for_status()
                data = response.json()
                
                if data.get('results') and len(data['results']) > 0:
                    logger.info(f"Found image for: {query}")
                    return data['results'][0]
                
                logger.warning(f"No images found for: {query}")
                return None
                
        except Exception as e:
            logger.error(f"Error searching Unsplash for '{query}': {str(e)}")
            return None
            
    async def get_random_photo(self, query: str = None) -> Optional[Dict[str, Any]]:
        """Get a random photo, optionally filtered by query."""
        params = {"count": 1}
        if query:
            params["query"] = query
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/photos/random", 
                    params=params,
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()[0] if isinstance(response.json(), list) else response.json()
        except Exception as e:
            logger.error(f"Error getting random photo: {str(e)}")
            return None

# Create a singleton instance
unsplash_service = UnsplashService()