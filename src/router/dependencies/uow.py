from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.service.uow import UnitOfWork

session_factory = sessionmaker(
    bind=create_async_engine(
    "postgresql+asyncpg://user:12345@localhost:5430/drone",
    echo=True,
    future=True
    ),
    class_=AsyncSession,
    autoflush=False
)

uow = UnitOfWork(session_factory=session_factory)

def get_uow():
    return uow
