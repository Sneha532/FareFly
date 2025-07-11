import google.generativeai as genai
from typing import List, Dict, Any
from src.app.core.config import settings
import logging
import json
import re

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    async def get_place_recommendations(self, 
                                     destination: str, 
                                     interests: List[str] = None, 
                                     duration_days: int = 3,
                                     budget: str = "medium") -> List[Dict[str, Any]]:
        """Get tourist place recommendations based on destination and preferences."""
        try:
            interests_str = ", ".join(interests) if interests and isinstance(interests, list) else "general sightseeing"
            
            # Updated prompt to include image keywords
            prompt = f"""
            Generate tourist attraction recommendations for {destination} for a {duration_days}-day trip 
            with a {budget} budget. The traveler is interested in {interests_str}.
            
            Return your response as a valid JSON array of objects, each with these fields:
            - name: Name of the attraction
            - description: Brief description (50-100 words)
            - category: Type of attraction (historical, natural, cultural)
            - estimated_time: Numeric hours to visit
            - estimated_cost: Numeric cost in USD
            - best_time_to_visit: Best time of day or season
            - image_keywords: 2-3 specific keywords for finding relevant images
            
            Format your entire response as valid JSON only, with no other text.
            """
            
            logger.info(f"Sending request to Gemini API for {destination}")
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                logger.error("Empty response from Gemini API")
                return self.get_fallback_recommendations(destination)
                
            logger.info(f"Received response from Gemini API: {response.text[:100]}...")
            
            # Try to parse the response
            attractions = self.parse_gemini_response(response.text)
            
            # If parsing fails, use fallback
            if not attractions:
                logger.warning("Failed to parse Gemini response, using fallback")
                return self.get_fallback_recommendations(destination)
                
            return attractions
            
        except Exception as e:
            logger.error(f"Error getting recommendations from Gemini: {str(e)}")
            return self.get_fallback_recommendations(destination)
    
    def parse_gemini_response(self, response_text: str) -> List[Dict[str, Any]]:
        """Parse the Gemini API response to extract structured data."""
        try:
            # Clean the response to extract just JSON content
            # First try to find JSON content with regex
            json_match = re.search(r'\[\s*\{.*\}\s*\]', response_text, re.DOTALL)
            
            if json_match:
                content = json_match.group(0)
                return json.loads(content)
            
            # If no match with regex, try other patterns
            if response_text.strip().startswith("[") and response_text.strip().endswith("]"):
                return json.loads(response_text)
            
            # Look for code block markers
            code_block_match = re.search(r'```(?:json)?\s*(\[.*?\])\s*```', response_text, re.DOTALL)
            if code_block_match:
                content = code_block_match.group(1)
                return json.loads(content)
            
            # If all else fails, try to find any JSON-like structure
            content = re.sub(r'^[^[]*', '', response_text)
            content = re.sub(r'[^\]]*$', '', content)
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Error parsing Gemini response: {str(e)}")
            logger.error(f"Original response: {response_text[:200]}...")
            return []
            
    def get_fallback_recommendations(self, destination: str) -> List[Dict[str, Any]]:
        """Provide fallback recommendations if Gemini API fails."""
        # Generic recommendations that work for most cities
        return [
            {
                "name": f"{destination} City Center",
                "description": f"Explore the historic heart of {destination} with its diverse architecture, local shops, and vibrant atmosphere.",
                "category": "cultural",
                "estimated_time": 3,
                "estimated_cost": 0,
                "best_time_to_visit": "Morning or late afternoon"
            },
            {
                "name": f"{destination} Museum",
                "description": f"Discover the rich history and cultural heritage of {destination} through fascinating exhibits and artifacts.",
                "category": "historical",
                "estimated_time": 2,
                "estimated_cost": 15,
                "best_time_to_visit": "Weekday mornings"
            },
            {
                "name": f"{destination} Local Market",
                "description": f"Experience the authentic flavors and crafts of {destination} at this bustling market filled with local vendors.",
                "category": "cultural",
                "estimated_time": 2,
                "estimated_cost": 10,
                "best_time_to_visit": "Morning"
            }
        ]

# Create a singleton instance
gemini_service = GeminiService()