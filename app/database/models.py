from sqlalchemy import String, Integer, DateTime, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class MediaCache(Base):
    __tablename__ = 'media_cache'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    url_id: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    raw_url: Mapped[str] = mapped_column(String(512))
    media_type: Mapped[str] = mapped_column(String(10))                      
    tg_file_id: Mapped[str] = mapped_column(String(255), nullable=True)     
    downloaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)