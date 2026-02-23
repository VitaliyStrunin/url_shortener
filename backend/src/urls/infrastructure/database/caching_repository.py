import redis.asyncio as redis
import json

from src.urls.services.interfaces.short_url_repository import IShortURLRepository
from src.urls.domain.entities import ShortURL


class CachingShortURLRepository(IShortURLRepository):
    def __init__(self, repo: IShortURLRepository, 
                 redis_client: redis.Redis,
                 cache_ttl: int = 3600
                 ):
        self.repository = repo
        self.redis = redis_client
        self.cache_ttl = cache_ttl
        self.cache_prefix = "short_url:code:"
        self.analytics_prefix = "analytics:redirects:"
    
    
    def _get_cache_key(self, code: str) -> str:
        return f"{self.cache_prefix}{code}"
    
    def _get_analytics_key(self, code: str) -> str:
        return f"{self.analytics_prefix}{code}"
    
    
    async def get_short_url_by_code(self, code: str) -> ShortURL:
        cache_key = self._get_cache_key(code)
        cached_data = await self.redis.get(cache_key)
        
        if cached_data:
            return ShortURL(**json.loads(cached_data))
        
        url = await self.repository.get_short_url_by_code(code)
        if url:
            await self.redis.setex(
                cache_key,
                self.cache_ttl, 
                url.model_dump_json()
            )
            
        return url
    
    async def increment_redirect_amount(self, code):
        analytics_key = self._get_analytics_key(code)
        await self.redis.incr(analytics_key)
        await self.redis.expire(analytics_key, 86400)
        
    async def create_short_url(self):
        pass
    
    async def delete_short_url(self, id):
        pass
    
    async def get_short_url_by_id(self, id):
        pass