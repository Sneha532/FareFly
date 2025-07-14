/**
 * FareFly Frontend Configuration
 * This file contains environment-specific settings for the frontend application
 */

const ENV = {
  // API configuration
  API: {
    // Base URL - change this when deploying to production
    BASE_URL: "https://farefly-production.up.railway.app",
    
    // Local development URL (uncomment for local development)
    // BASE_URL: "http://127.0.0.1:8000",
    
    // API endpoints
    ENDPOINTS: {
      LOGIN: "/api/auth/login",
      REGISTER: "/api/auth/register",
      USER_PROFILE: "/api/auth/me",
      UPDATE_PROFILE: "/api/users/me",
      CHANGE_PASSWORD: "/api/users/password",
      USER_PREFERENCES: "/api/users/preferences",
      FLIGHT_SEARCH: "/api/flights/search",
      HOTEL_SEARCH: "/api/hotels/search",
      RECOMMENDATIONS: "/api/recommendations"
    }
  }
};

// Helper function to get full API URL
function getApiUrl(endpoint) {
  return ENV.API.BASE_URL + endpoint;
}