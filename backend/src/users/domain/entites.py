from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    hashed_password: str
    
    
class UserCreate(BaseModel):
    id: int
    username: str
    

class UserUpdate(BaseModel):
    id: int
    username: str | None
    hashed_password: str | None
    