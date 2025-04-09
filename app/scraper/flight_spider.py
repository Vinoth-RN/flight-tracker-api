# app/scraper/flight_spider.py

import scrapy
from datetime import datetime

class FlightStatsSpider(scrapy.Spider):
    name = "flightstats"
    custom_settings = {
        "LOG_LEVEL": "INFO"
    }

    def __init__(self, flight_number=None, flight_date=None, results=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flight_number = flight_number
        self.flight_date = flight_date
        self.results = results if results is not None else []
        self.logger.warning(f"[Spider Init] flight_number={self.flight_number}, flight_date={self.flight_date}")

    def start_requests(self):
        self.logger.warning("[Spider] start_requests called")

        if not self.flight_number or not self.flight_date:
            self.logger.error("Missing flight_number or flight_date in spider init")
            return

        airline_code = ''.join(filter(str.isalpha, self.flight_number))
        number = ''.join(filter(str.isdigit, self.flight_number))

        try:
            date_obj = datetime.strptime(self.flight_date, "%Y-%m-%d")
        except ValueError as ve:
            self.logger.error(f" Invalid flight_date format: {self.flight_date} - {ve}")
            return

        year, month, day = date_obj.year, date_obj.month, date_obj.day

        self.airline_code = airline_code
        self.number = number
        self.departure_date = self.flight_date

        url = f"https://www.flightstats.com/v2/flight-tracker/{airline_code}/{number}?year={year}&month={month}&date={day}"
        self.logger.info(f" Requesting detail page: {url}")

        yield scrapy.Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        self.logger.info(f" Parsing detail page for flight: {self.flight_number}")

        try:
            
            departure_airport = response.css("div.text-helper__TextHelper-sc-8bko4a-0.gmpNkd span::text").get()
            arrival_airport = response.css("div.text-helper__TextHelper-sc-8bko4a-0.gmpNkd + div span::text").get()

            time_blocks = response.css("div.ticket__TimesWrapper-sc-1rrbl5o-9 span[data-testid=time]::text").getall()
            departure_time = time_blocks[0].strip() if len(time_blocks) > 0 else None
            arrival_time = time_blocks[1].strip() if len(time_blocks) > 1 else None

            status_text = response.css("div.ticket__StatusWrapper-sc-1rrbl5o-8 span::text").get()
            status = status_text.strip() if status_text else "Scheduled"

            if not departure_airport or not arrival_airport:
                self.logger.warning(" Could not extract both origin and destination airport codes")
            if not departure_time or not arrival_time:
                self.logger.warning(" Could not extract both departure and arrival times")

            item = {
                "airline_code": self.airline_code,
                "flight_number": self.flight_number,
                "departure_date": self.departure_date,
                "origin": departure_airport,
                "destination": arrival_airport,
                "departure_time": departure_time,
                "arrival_time": arrival_time,
                "status": status
            }

            self.results.append(item)
            yield item

        except Exception as e:
            self.logger.error(f" Error parsing detail page: {e}")
