import sys
import os
import json


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, BASE_DIR)


from app.scraper.spider_runner import run_spider_core

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("[]")
        sys.exit(1)

    flight_number = sys.argv[1]
    flight_date = sys.argv[2]

    result = run_spider_core(flight_number, flight_date)

    print(json.dumps(result or []))
