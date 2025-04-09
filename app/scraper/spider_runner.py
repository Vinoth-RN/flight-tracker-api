# app/scraper/spider_runner.py

import os
import sys
import logging
from twisted.internet import asyncioreactor
try:
    asyncioreactor.install()
except Exception:
    pass

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import defer, reactor
from app.scraper.flight_spider import FlightStatsSpider

def run_spider_core(flight_number: str, flight_date: str):
    print(f"[spider_runner]  Running core spider for flight {flight_number} on {flight_date}", file=sys.stderr)
    results = []

    runner = CrawlerRunner(settings={
        "LOG_LEVEL": "INFO",
        "ITEM_PIPELINES": {
            "app.scraper.pipelines.StoreFlightDataPipeline": 300,
        },
        "FEEDS": {
            "stdout:": {
                "format": "json",
                "overwrite": True,
            }
        }
    })

    @defer.inlineCallbacks
    def crawl():
        try:
            yield runner.crawl(FlightStatsSpider, flight_number=flight_number, flight_date=flight_date)
        finally:
            reactor.stop()

    try:
        crawl()
        reactor.run()
    except Exception as e:
        print(f"[spider_runner]  Error in reactor: {e}", file=sys.stderr)

    return results
