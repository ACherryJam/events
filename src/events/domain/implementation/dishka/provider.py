from dishka import Provider, Scope, provide

from events.domain.dispatcher import DomainEventDispatcher
from events.domain.event_handler.factory import DomainEventHandlerFactory
from events.domain.event_handler.handler import DomainEventHandler, DomainEventHandlerRegistry
from events.domain.implementation.dishka.factory import DishkaDomainEventHandlerFactory


class DomainEventImplementationProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_handler_registry(self) -> DomainEventHandlerRegistry:
        return DomainEventHandler.registry
    
    factory = provide(
        provides=DomainEventHandlerFactory,
        source=DishkaDomainEventHandlerFactory,
        scope=Scope.REQUEST
    )

    dispatcher = provide(
        DomainEventDispatcher,
        scope=Scope.REQUEST
    )
