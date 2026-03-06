import redis.asyncio as redis
from src.core.config import settings

redis_pool = redis.ConnectionPool.from_url(
    settings.redis_url,
    encoding="utf-8", 
    decode_responses=True,
    max_connections=30
)


def get_redis_client() -> redis.Redis:
    return redis.Redis(connection_pool=redis_pool)