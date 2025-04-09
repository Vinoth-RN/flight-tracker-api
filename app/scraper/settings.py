

BOT_NAME = "flightstats_scraper"

SPIDER_MODULES = ["app.scraper"]
NEWSPIDER_MODULE = "app.scraper"

ROBOTSTXT_OBEY = False

LOG_LEVEL = "INFO"

ITEM_PIPELINES = {
    "app.scraper.pipelines.StoreFlightDataPipeline": 300,
}


RETRY_ENABLED = False


DOWNLOAD_TIMEOUT = 15
