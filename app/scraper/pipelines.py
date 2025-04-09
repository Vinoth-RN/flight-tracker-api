# app/scraper/pipelines.py

import logging
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import SessionLocal
from app.models import FlightInfo

logger = logging.getLogger(__name__)


class StoreFlightDataPipeline:
    def open_spider(self, spider):
        self.db: Session = SessionLocal()
        logger.info("[Pipeline] DB session opened")

    def close_spider(self, spider):
        self.db.close()
        logger.info("[Pipeline] DB session closed")

    def parse_time(self, time_str):
        if not time_str:
            return None
        try:
            return datetime.strptime(time_str.strip(), "%I:%M %p").time()
        except Exception as e:
            logger.warning(f"[Pipeline] Failed to parse time '{time_str}': {e}")
            return None

    def process_item(self, item, spider):
        try:
            flight = FlightInfo(
                airline_code=item.get("airline_code"),
                flight_number=item.get("flight_number"),
                departure_date=datetime.strptime(item.get("departure_date"), "%Y-%m-%d").date(),
                origin=item.get("origin"),
                destination=item.get("destination"),
                departure_time=self.parse_time(item.get("departure_time")),
                arrival_time=self.parse_time(item.get("arrival_time")),
                status=item.get("status"),
            )

            logger.info(f"[Pipeline] Saving flight to DB: {flight.flight_number} on {flight.departure_date}")
            self.db.add(flight)
            self.db.commit()
            self.db.refresh(flight)

        except Exception as e:
            logger.error(f"[Pipeline] Error saving flight data: {e}")
            self.db.rollback()

        return item
