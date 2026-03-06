from abc import ABC, abstractmethod
from src.users.domain.entites import User, UserCreate, UserUpdate


class IUserRepository(ABC):
    async def add(self, user: UserCreate) -> User | None:
        pass
    
    async def get_by_id(self, id: int) -> User | None:
        pass
    
    async def update(self, user: UserUpdate) -> User | None:
        pass
    
    async def delete(self, id: int) -> bool:
        pass