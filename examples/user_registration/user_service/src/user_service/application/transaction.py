import abc
from typing import Protocol


class Transaction(Protocol):
    @abc.abstractmethod
    async def commit(self):
        ...

    @abc.abstractmethod
    async def rollback(self):
        ...
