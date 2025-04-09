from sqlalchemy import Column, Integer, String, Date, Time
from app.database import Base

class FlightInfo(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    airline_code = Column(String, index=True)
    flight_number = Column(String, index=True)
    departure_date = Column(Date, index=True)

    origin = Column(String)
    destination = Column(String)

    departure_time = Column(Time, nullable=True)
    arrival_time = Column(Time, nullable=True)

    status = Column(String)
