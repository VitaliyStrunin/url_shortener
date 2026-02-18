from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi import Request
from fastapi.responses import JSONResponse

from src.core.exceptions import ImpossibleToAddURL, ShortURLNotFoundByID, ShortURLNotFoundByCode
from src.database.engine import engine
from src.database.base import Base
from src.urls.presentation.api.routes import short_urls_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(short_urls_router)

@app.exception_handler(ImpossibleToAddURL)
async def impossible_to_add_url_handler(request: Request, exception: ImpossibleToAddURL):
    return JSONResponse(status_code=500, content={"detail": str(exception)})

@app.exception_handler(ShortURLNotFoundByID)
async def url_not_found_by_id_handler(request: Request, exception: ShortURLNotFoundByID):
    return JSONResponse(status_code=404, content={"detail": str(exception)})

@app.exception_handler(ShortURLNotFoundByCode)
async def url_not_found_by_code_handler(request: Request, exception: ShortURLNotFoundByCode):
    return JSONResponse(status_code=404, content={"detail": str(exception)})
