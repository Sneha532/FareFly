from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey, Float, ARRAY
from sqlalchemy.orm import relationship
import datetime

from src.app.db.base_class import Base
from src.app.models.user import User

class Flight(Base):  
    __tablename__ = "flight"

    booking_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey(User.user_id), nullable=False)
    flight_id = Column(String, nullable=False)
    total_price = Column(String, nullable=False)
    booking_date = Column(DateTime, default=datetime.datetime.utcnow)
    departure_date = Column(DateTime, nullable=False)
    arrival_date = Column(DateTime, nullable=False)
    departure_location = Column(String, nullable=False)
    arrival_location = Column(String, nullable=False)
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Correct relationship to User
    user = relationship("User", back_populates="flights")  # Changed from itineraries