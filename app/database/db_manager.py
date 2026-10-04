from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.database.models import Base, User, MediaCache
from sqlalchemy import select

DATABASE_URL = "sqlite+aiosqlite:///downloader.db"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def register_user(tg_id: int):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(User).where(User.tg_id == tg_id))
            user = result.scalar_one_or_none()
            if not user:
                session.add(User(tg_id=tg_id))

async def get_cached_media(url_id: str, media_type: str):
    async with async_session() as session:
        result = await session.execute(
            select(MediaCache).where(MediaCache.url_id == url_id, MediaCache.media_type == media_type)
        )
        return result.scalar_one_or_none()

async def save_url_to_cache(url_id: str, raw_url: str, media_type: str):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(MediaCache).where(MediaCache.url_id == url_id, MediaCache.media_type == media_type))
            if not result.scalar_one_or_none():
                session.add(MediaCache(url_id=url_id, raw_url=raw_url, media_type=media_type))

async def update_file_id_in_cache(url_id: str, media_type: str, file_id: str):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(MediaCache).where(MediaCache.url_id == url_id, MediaCache.media_type == media_type)
            )
            cache_entry = result.scalar_one_or_none()
            if cache_entry:
                cache_entry.tg_file_id = file_id