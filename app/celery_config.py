from celery import Celery

celery_app = Celery(
    "flight_tracker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

celery_app.conf.task_routes = {
    "app.tasks.run_scraper": {"queue": "scraper"},
}
