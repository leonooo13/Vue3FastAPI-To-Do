from typing import Generator, AsyncGenerator

from sqlmodel import create_engine, Session
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import User, Task

DATABASE_URL = "sqlite:///./FastBox.db"
engine = create_engine(DATABASE_URL, echo=True)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session_maker() as session:
#         yield session
