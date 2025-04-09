import sys
import os
from scrapy.crawler import CrawlerProcess


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, BASE_DIR)

from app.scraper.flight_spider import FlightStatsSpider
from app.scraper import pipelines 

def run_spider(flight_number, flight_date):
    process = CrawlerProcess(settings={
        "LOG_LEVEL": "INFO",
        "ITEM_PIPELINES": {
            "app.scraper.pipelines.StoreFlightDataPipeline": 300,
        },
    })

    process.crawl(FlightStatsSpider, flight_number=flight_number, flight_date=flight_date)
    process.start()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python run_spider.py <FLIGHT_NUMBER> <FLIGHT_DATE>")
        sys.exit(1)

    flight_number = sys.argv[1]
    flight_date = sys.argv[2]
    run_spider(flight_number, flight_date)
