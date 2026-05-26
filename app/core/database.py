from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from .config import DATABASE_URL


engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
           await db.close()