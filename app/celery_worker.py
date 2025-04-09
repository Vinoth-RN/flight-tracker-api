from app.celery_config import celery_app

celery_app.autodiscover_tasks(["app.tasks"])

# to be run via CLI 
