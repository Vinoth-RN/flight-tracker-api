from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.database import SessionLocal, init_db
from app.crud import save_flight_info, get_flight_by_details
from app.tasks import run_scraper

app = FastAPI(title="Flight Tracker API")

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/flight-info")
def get_flight_info(
    airline_code: str = Query(...),
    flight_number: str = Query(...),
    departure_date: str = Query(...)
):
    db = SessionLocal()
    flight = get_flight_by_details(db, airline_code, flight_number, departure_date)
    db.close()

    if flight:
        return JSONResponse(content=flight)

    return JSONResponse(
        content={"message": "Flight info not found. Use /scrape to fetch."},
        status_code=404,
    )


def handle_scrape_request(airline_code: str, flight_number: str, departure_date: str):
    db = SessionLocal()
    existing_flight = get_flight_by_details(db, airline_code, flight_number, departure_date)
    db.close()

    if existing_flight:
        return JSONResponse(content={
            "message": "Flight data already exists in database.",
            "flight_data": existing_flight
        })

    full_flight_number = f"{airline_code}{flight_number}"
    run_scraper.delay(full_flight_number, departure_date)

    return {
        "message": f"Scraping for {full_flight_number} on {departure_date} has started."
    }


class ScrapeRequest(BaseModel):
    flight_number: str  # full like EK547
    flight_date: str    # format YYYY-MM-DD

@app.post("/scrape")
def scrape_flight_post(request: ScrapeRequest):
    airline_code = request.flight_number[:2]
    flight_number = request.flight_number[2:]
    return handle_scrape_request(airline_code, flight_number, request.flight_date)

# NEW GET endpoint (using query params)
@app.get("/scrape")
def scrape_flight_get(
    airline_code: str = Query(...),
    flight_number: str = Query(...),
    departure_date: str = Query(...)
):
    return handle_scrape_request(airline_code, flight_number, departure_date)
