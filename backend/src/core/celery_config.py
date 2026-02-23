from celery import Celery
from celery.signals import worker_shutdown
import redis.asyncio as redis
import asyncio

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


celery_redis_client = redis.Redis.from_url(
    settings.redis_url,
    encoding="utf-8",
    decode_responses=True,
    max_connections=5 
)

@worker_shutdown.connect
def shutdown_redis(**kwargs):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(celery_redis_client.close())