from sqlalchemy.ext.asyncio import AsyncSession

from user_service.application.transaction import Transaction


class SQLAlchemyTransaction(Transaction):
    def __init__(
        self,
        session: AsyncSession
    ):
        self.session = session

    async def commit(self):
        await self.session.commit()
    
    async def rollback(self):
        await self.session.rollback()    
    