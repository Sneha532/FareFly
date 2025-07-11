from sqlalchemy import Boolean, Column, String, DateTime,ForeignKey, Float, ARRAY
from sqlalchemy.orm import relationship
import datetime

from src.app.db.base_class import Base  # Fixed import
from src.app.models.user import User  # Import User model

class Flight(Base):  
    __tablename__ = "flight"  # Explicitly set the table name

    booking_id= Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey(User.user_id), nullable=False)
    flight_id = Column(String, nullable=False)
    total_price = Column(String, nullable=False)  # Assuming price is stored as a string for simplicity
    booking_date = Column(DateTime, default=datetime.datetime.utcnow)
    departure_date = Column(DateTime, nullable=False)
    arrival_date = Column(DateTime, nullable=False)
    departure_location = Column(String, nullable=False)
    arrival_location = Column(String, nullable=False)
    status = Column(String, default="Pending")  # Booking status (e.g., Pending
    # Confirmed, Cancelled)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow) 

        # Relationships
    itineraries = relationship("Itinerary", back_populates="user")