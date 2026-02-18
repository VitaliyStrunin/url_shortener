from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from src.urls.domain.entities import ShortURL, ShortURLCreate
from src.urls.services.interfaces.short_url_repository import IShortURLRepository
from src.urls.infrastructure.database.orm import ShortURLDB


class PostgresShortURLRepository(IShortURLRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create_short_url(self, short_url: ShortURLCreate) -> ShortURL:
        url = ShortURLDB(**short_url.model_dump())
        self.session.add(url)
        await self.session.commit()
        return ShortURL.model_validate(url)
    
    async def get_short_url_by_id(self, id: int) -> ShortURL | None:
        url = await self.session.get(ShortURLDB, id)
        if url: 
            url = ShortURL.model_validate(url)
        return url
        
    async def get_short_url_by_code(self, code: str) -> ShortURL | None:
        query = select(ShortURLDB).where(ShortURLDB.code == code)
        result = await self.session.execute(query)
        url = result.scalar_one_or_none()
        if url:
            return ShortURL.model_validate(url)
        return url
        
    async def delete_short_url(self, id: int) -> bool:
        url = await self.session.get(ShortURLDB, id)
        if not url:
            return False
        await self.session.delete(url)
        return True
    
    
    async def increment_redirect_amount(self, code: str) -> None:
        await self.session.execute(
            update(ShortURLDB)
            .where(ShortURLDB.code == code)
            .values(redirect_amount=ShortURLDB.redirect_amount + 1)
        )
        await self.session.commit()