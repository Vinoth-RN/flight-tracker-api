# app/tasks.py

from app.celery_config import celery_app
from app.scraper.run_spider import run_spider
from app.database import SessionLocal
from app.crud import save_flight_info

@celery_app.task(name="app.tasks.run_scraper")
def run_scraper(flight_number: str, departure_date: str):
    print(f"[Celery Task] Starting scraper for flight_number={flight_number}, departure_date={departure_date}")

    try:
        scraped_data = run_spider(flight_number, departure_date)
    except Exception as e:
        print(f"[Celery Task] Spider failed: {e}")
        return

    if not scraped_data:
        print("[Celery Task] No data scraped.")
        return

    print(f"[Celery Task] Scraped {len(scraped_data)} items.")

    db = SessionLocal()
    try:
        for item in scraped_data:
            print(f"[Celery Task] Saving item: {item}")
            save_flight_info(db, item)
    except Exception as e:
        print(f"[Celery Task] Error saving to DB: {e}")
    finally:
        db.close()
        print("[Celery Task] DB session closed.")
