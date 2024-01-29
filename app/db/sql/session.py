from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import async_session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as db_session:
        try:
            yield db_session
            await db_session.commit()
        except Exception as e:
            await db_session.rollback()
            raise e
        finally:
            await db_session.close()
