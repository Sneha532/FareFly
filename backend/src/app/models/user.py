from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.orm import relationship
import datetime

from src.app.db.base_class import Base  # Fixed import

class User(Base):
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean(), default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    itineraries = relationship("Itinerary", back_populates="user")