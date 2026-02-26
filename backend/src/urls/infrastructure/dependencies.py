from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis

from src.urls.services.short_url_service import ShortURLService
from src.urls.infrastructure.database.caching_repository import CachingShortURLRepository
from src.urls.infrastructure.database.repository import PostgresShortURLRepository
from src.database.redis.redis import get_redis_client
from src.database.engine import get_async_db_session


async def get_short_url_service(db_session: AsyncSession = Depends(get_async_db_session), redis_client: redis.Redis = Depends(get_redis_client)):
    repository = PostgresShortURLRepository(db_session)
    caching_repository = CachingShortURLRepository(repository, redis_client)
    return ShortURLService(caching_repository)