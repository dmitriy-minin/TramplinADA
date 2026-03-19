from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_db_tables():
    from app.models import user, company, opportunity, application  # noqa
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed_admin()


async def seed_admin():
    from app.models.user import User, UserRole
    from app.core.security import get_password_hash
    from app.core.config import settings
    from sqlalchemy import select

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.email == settings.ADMIN_EMAIL)
        )
        if result.scalar_one_or_none():
            return

        admin = User(
            email=settings.ADMIN_EMAIL,
            hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
            full_name=settings.ADMIN_NAME,
            role=UserRole.CURATOR,
            is_verified=True,
            is_active=True,
            is_main_admin=True,
        )
        session.add(admin)
        await session.commit()
        print(f"✅ Главный администратор создан: {settings.ADMIN_EMAIL}")
