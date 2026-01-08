from typing import AsyncIterable
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from dishka import Provider, Scope, from_context, provide

from user_service.application.transaction import Transaction
from user_service.domain.user.repository import UserRepository
from user_service.infrastructure.persistence.models.base import BaseModel
from user_service.infrastructure.persistence.models.user.repository import SQLUserRepository
from user_service.infrastructure.persistence.outbox import Outbox, SQLOutbox
from user_service.infrastructure.persistence.settings import SQLPersistenceSettings
from user_service.infrastructure.persistence.transaction import SQLAlchemyTransaction


class SQLAlchemyPersistenceProvider(Provider):
    settings = from_context(
        SQLPersistenceSettings,
        scope=Scope.APP
    )

    @provide(scope=Scope.APP)
    async def provide_engine(self, settings: SQLPersistenceSettings) -> AsyncIterable[AsyncEngine]:
        engine = create_async_engine(
            url=settings.database_url,
            pool_pre_ping=True,
            pool_recycle=3600,
        )

        # Used only for easier setup of database
        # In real application one should use alembic migrations to define DB schema
        async with engine.connect() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)

        yield engine
        await engine.dispose()
    
    @provide(scope=Scope.REQUEST) 
    async def provide_session(self, engine: AsyncEngine) -> AsyncIterable[AsyncSession]:
        session = AsyncSession(engine)
        yield session
        await session.close()

    @provide(scope=Scope.REQUEST)
    async def provide_transaction(self, session: AsyncSession) -> Transaction:
        return SQLAlchemyTransaction(session)
    
    user_repository = provide(
        provides=UserRepository,
        source=SQLUserRepository,
        scope=Scope.REQUEST
    )

    outbox = provide(
        provides=Outbox,
        source=SQLOutbox,
        scope=Scope.REQUEST
    )
