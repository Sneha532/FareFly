from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.api.routes import api_router
from src.app.core.config import settings

app = FastAPI(
    title="FareFly API",
    description="API for FareFly travel booking application",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all API routes
app.include_router(api_router, prefix="/api")

@app.get("/")       
async def root():
    return {"message": "Welcome to FareFly API"}