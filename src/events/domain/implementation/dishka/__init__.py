from importlib.util import find_spec
if find_spec("dishka") is None:
    raise ImportError("To use this implementation make sure dishka is installed")

from .factory import DishkaDomainEventHandlerFactory
from .provider import DomainEventImplementationProvider


__all__ = [
    "DishkaDomainEventHandlerFactory",
    "DomainEventImplementationProvider"
]
