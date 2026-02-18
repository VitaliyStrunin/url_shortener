from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from pydantic import HttpUrl
from src.core.config import CODE_LENGTH
from src.database.base import Base


class ShortURLDB(Base):
    __tablename__ = "short_urls"
    
    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    
    code: Mapped[str] = mapped_column(
        String(CODE_LENGTH), 
        nullable=False,
        unique=True, 
        index=True
    )
    
    redirect_to: Mapped[str] = mapped_column(
        String(1000),
        nullable=False, 
        index=True
    )
    
    redirect_amount: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )