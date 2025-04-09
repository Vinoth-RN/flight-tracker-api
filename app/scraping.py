
def scrape_flight_info(airline_code: str, flight_number: str, departure_date: str):
    
    return {
        "airline_code": airline_code,
        "flight_number": flight_number,
        "departure_date": departure_date,
        "status": "On Time",
        "origin": "JFK",
        "destination": "LAX"
    }
