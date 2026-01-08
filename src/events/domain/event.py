import abc
from typing import Protocol


class DomainEvent(Protocol):
    @property
    @abc.abstractmethod
    def type(self) -> str:
        ...
