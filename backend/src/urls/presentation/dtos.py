from pydantic import BaseModel, HttpUrl


class ShortURLReadDTO(BaseModel):
    code: str
    redirect_to: HttpUrl
    redirect_amount: int
    
    
class ShortURLCreateDTO(BaseModel):
    redirect_to: HttpUrl
    