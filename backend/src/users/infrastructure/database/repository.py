from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from src.users.domain.entites import User, UserCreate, UserUpdate
from src.users.services.interfaces.user_repository import IUserRepository
from src.users.infrastructure.database.orm import UserDB
from src.core.exceptions import UserAlreadyExists, UserNotFound


class PostgresUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.__session = session
    
    async def add(self, user: UserCreate) -> User | None:
        db_user = UserDB(**user.model_dump())
        try:
            self.__session.add(db_user)
            await self.__session.commit()
            await self.__session.refresh(db_user)
            return User.model_validate(db_user.__dict__)
        except IntegrityError:
            await self.__session.rollback()
            raise UserAlreadyExists(user.username)

    async def get_by_id(self, id: int) -> User:
        user = await self.__session.get(UserDB, pk=id)
        if not user:
            raise UserNotFound(f"ID: {id}")
        return User.model_validate(user.__dict__)
    
    async def get_by_username(self, username: str) -> User:
        query = select(UserDB).where(UserDB.username==username)
        result = await self.__session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise UserNotFound(f"Username: {username}")
        return User.model_validate(user.__dict__)
    
    async def delete(self, id: int):
        user = await self.__session.get(UserDB, id)
        if not user:
            raise UserNotFound(f"ID: {id}")
        await self.__session.delete(user)
        await self.__session.commit()
        
    async def update(self, user_update: UserUpdate) -> User:
        user = await self.__session.get(UserDB, user_update.id)
        if not user:
            raise UserNotFound(f"ID: {user_update.id}")
        for field, value in user_update.model_dump(exclude_unset=True):
            if value is not None:
                setattr(user, field, value)
        await self.__session.commit()
        await self.__session.refresh(user)
        return User.model_validate(user.__dict__)
    