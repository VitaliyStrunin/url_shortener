from pydantic import BaseModel, ConfigDict, HttpUrl


class ShortURL(BaseModel):
    id: int
    code: str
    redirect_to: HttpUrl
    redirect_amount: int
    
    model_config = ConfigDict(from_attributes=True)
    
    
class ShortURLCreate(BaseModel):
    code: str
    redirect_to: str
    redirect_amount: int = 0
    
    model_config = ConfigDict(from_attributes=True)
    