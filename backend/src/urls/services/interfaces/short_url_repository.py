from abc import ABC, abstractmethod
from src.urls.domain.entities import ShortURL, ShortURLCreate

class IShortURLRepository(ABC):
    @abstractmethod
    async def create_short_url(self, short_url: ShortURLCreate) -> ShortURL:
        pass
    
    @abstractmethod
    async def get_short_url_by_id(self, id: int) -> ShortURL | None:
        pass
    
    @abstractmethod
    async def get_short_url_by_code(self, code: str) -> ShortURL | None:
        pass
    
    @abstractmethod
    async def delete_short_url(self, id: int) -> bool:
        pass
    
    @abstractmethod
    async def increment_redirect_amount(self, code: str) -> None:
        pass
    