from src.urls.services.interfaces.short_url_repository import IShortURLRepository
from src.urls.presentation.dtos import ShortURLCreateDTO
from src.urls.domain.entities import ShortURL, ShortURLCreate
from src.core.config import settings
from src.core.utils import generate_random_code
from src.core.exceptions import ImpossibleToAddURL, ShortURLNotFoundByCode, ShortURLNotFoundByID


class ShortURLService:
    def __init__(self, url_repository: IShortURLRepository):
        self.repository = url_repository
        
    async def create_short_url(self, url_create_dto: ShortURLCreateDTO) -> ShortURL:
        for _ in range(settings.MAX_CODE_GENERATION_ATTEMPTS):
            random_code = generate_random_code()
            url = await self.repository.get_short_url_by_code(random_code)
            if not url:
                break     
        else:
            raise ImpossibleToAddURL(f"Can't create unique code after {settings.MAX_CODE_GENERATION_ATTEMPTS} attempts")
        
        create_data = {
            "code": random_code,
            "redirect_to": str(url_create_dto.redirect_to)
        }
        
        url_create = ShortURLCreate.model_validate(create_data)
        created_url = await self.repository.create_short_url(url_create)
        return created_url
        
    async def get_url_by_id(self, short_url_id: int) -> ShortURL:
        url = await self.repository.get_short_url_by_id(short_url_id)
        if not url:
            raise ShortURLNotFoundByCode(short_url_id)
        return url
    
    async def get_url_by_code(self, code: str) -> ShortURL:
        url = await self.repository.get_short_url_by_code(code)
        if not url:
            raise ShortURLNotFoundByCode(code)
        return url
    
    async def delete_url(self, short_url_id: int) -> bool:
        deleted = await self.repository.delete_short_url(short_url_id)
        if not deleted:
            raise ShortURLNotFoundByID(short_url_id)
        return True
    
    async def redirect(self, code: str) -> ShortURL:
        url = await self.repository.get_short_url_by_code(code)
        if not url:
            raise ShortURLNotFoundByCode(code)
        
        await self.repository.increment_redirect_amount(code)
        return url