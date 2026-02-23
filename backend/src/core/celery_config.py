from celery import Celery
from src.core.config import settings


celery_app = Celery(
    "url_shortener",
    broker=settings.redis_url,
    include=['src.urls.infrastructure.tasks']
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
    "sync-analytics-every-minute": {
        "task": "sync_analytics_to_db",
        "schedule": 60.0,
        },
    },
)
