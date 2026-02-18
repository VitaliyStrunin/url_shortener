from abc import ABC, abstractmethod
from src.urls.domain.entities import ShortURL, ShortURLCreate

class IShortURLRepository(ABC):
    async def create_short_url(self, short_url: ShortURLCreate) -> ShortURL:
        pass
    
    async def get_short_url_by_id(self, id: int) -> ShortURL | None:
        pass
    
    async def get_short_url_by_code(self, code: str) -> ShortURL | None:
        pass
    
    async def delete_short_url(self, id: int) -> bool:
        pass
    
    async def increment_redirect_amount(self, code: str) -> None:
        pass