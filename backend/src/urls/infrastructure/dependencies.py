from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.urls.services.short_url_service import ShortURLService
from src.urls.infrastructure.database.repository import PostgresShortURLRepository
from src.database.engine import get_async_db_session


async def get_short_url_service(db_session: AsyncSession = Depends(get_async_db_session)):
    repository = PostgresShortURLRepository(db_session)
    return ShortURLService(repository)