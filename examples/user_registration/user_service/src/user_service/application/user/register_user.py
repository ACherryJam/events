from events.domain.dispatcher import DomainEventDispatcher

from user_service.application.transaction import Transaction
from user_service.domain.user.entity import User
from user_service.domain.user.repository import UserRepository


class RegisterUserInteractor:
    def __init__(
        self,
        repository: UserRepository,
        dispatcher: DomainEventDispatcher,
        transaction: Transaction
    ) -> None:
        self.repository = repository
        self.dispatcher = dispatcher
        self.transaction = transaction

    async def __call__(self, email: str, password: str) -> None:
        try:
            user_id = await self.repository.get_next_id()
            user = User(user_id, email, password)
            user.initialize()

            self.dispatcher.from_entity(user)
            await self.dispatcher.process()
            
            await self.repository.insert(user)
            await self.transaction.commit()
        except:
            await self.transaction.rollback()
            raise
        