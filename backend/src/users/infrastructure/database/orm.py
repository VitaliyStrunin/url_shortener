from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base

class UserDB(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(length=50),
        unique=True,
        index=True,
        nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024),
        nullable=False
    )