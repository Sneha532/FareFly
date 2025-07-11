from sqlalchemy import Boolean, Column, String, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
import datetime
import uuid
from src.app.models.user import User  # Ensure this import is correct
from src.app.db.base_class import Base  # Fixed import

class Itinerary(Base):
    __tablename__ = "itinerary"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    user_id = Column(String, ForeignKey(User.user_id))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    is_public = Column(Boolean, default=False)
    
    # Store flights, hotels, attractions as JSON
    flights = Column(JSON, default=list)
    hotels = Column(JSON, default=list)
    attractions = Column(JSON, default=list)
    
    # Relationships
    user = relationship("User", back_populates="itineraries")