from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey

from src.core.config import settings
from src.database.base import Base
from src.users.infrastructure.database.orm import UserDB


class ShortURLDB(Base):
    __tablename__ = "short_urls"
    
    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    
    code: Mapped[str] = mapped_column(
        String(settings.CODE_LENGTH), 
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
    
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", on_delete="SET NULL"),
        nullable=True
        
    )
    
    owner: Mapped["UserDB | None"] = relationship(
        back_populates="short_urls"
    )