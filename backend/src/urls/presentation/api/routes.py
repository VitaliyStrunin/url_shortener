from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
import logging

from src.urls.presentation.dtos import ShortURLCreateDTO, ShortURLReadDTO
from src.urls.services.short_url_service import ShortURLService
from src.urls.infrastructure.dependencies import get_short_url_service

short_urls_logger = logging.getLogger(__name__)

short_urls_router = APIRouter(prefix="/url")

@short_urls_router.post("/", response_model=ShortURLReadDTO)
async def create_url(
    create_dto: ShortURLCreateDTO,
    service: ShortURLService = Depends(get_short_url_service)
):
    created_url = await service.create_short_url(create_dto)
    return created_url


@short_urls_router.get("/{code}")
async def redirect_user_by_code(
    code: str, 
    service: ShortURLService = Depends(get_short_url_service)
):
    short_url = await service.redirect(code)
    url_to_redirect = short_url.redirect_to
    return RedirectResponse(url=url_to_redirect, status_code=302)