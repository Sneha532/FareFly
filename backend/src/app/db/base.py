# Import all the models so that Alembic can detect them
from src.app.db.base_class import Base
from src.app.models.user import User
from src.app.models.itinerary import Itinerary
from src.app.models.flight import Flight
from src.app.models.hotel import Hotel