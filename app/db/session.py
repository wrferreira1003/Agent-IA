# app/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from typing import AsyncGenerator

# Engine assíncrono para o SQLAlchemy
engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)

# Fábrica de sessões assíncronas
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependência FastAPI para obter uma sessão de banco de dados.
    Garante que a sessão seja sempre fechada após a requisição.
    """
    async with AsyncSessionLocal() as session:
        yield session