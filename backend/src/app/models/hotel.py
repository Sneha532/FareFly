from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey, Float, ARRAY
from sqlalchemy.orm import relationship
import datetime
from src.app.models.user import User  # Fixed import
from src.app.db.base_class import Base  # Fixed import

class Hotel(Base):
    __tablename__ = "hotel" 

    hotel_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey(User.user_id), nullable=False)
    total_price = Column(Float, nullable=False)  # Assuming price is stored as a float
    check_in_date = Column(DateTime, nullable=False)
    check_out_date = Column(DateTime, nullable=False)
    amenities = Column(ARRAY(String), nullable=True)  # Assuming amenities is a list of
    booking_date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="Pending")  # Booking status (e.g., Pending
    room_details=Column(ARRAY(String),nullable=False)
    hotel_location=Column(String,nullable=False)
    # Relationships
    user = relationship("User", back_populates="hotels")  # Changed from itineraries