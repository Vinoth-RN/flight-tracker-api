from sqlalchemy.orm import Session
from app.models import FlightInfo

def save_flight_info(db: Session, flight_data: dict):
    flight = FlightInfo(**flight_data)
    db.add(flight)
    db.commit()

def get_flight_by_details(db: Session, airline_code: str, flight_number: str, departure_date: str):
    flight = db.query(FlightInfo).filter_by(
        airline_code=airline_code,
        flight_number=flight_number,
        departure_date=departure_date
    ).first()
    if flight:
        return {
            "airline_code": flight.airline_code,
            "flight_number": flight.flight_number,
            "departure_date": flight.departure_date,
            "status": flight.status,
            "origin": flight.origin,
            "destination": flight.destination
        }
    return None
