from dishka import Provider, Scope, provide_all

from .user_registered import UserRegisteredEventHandler


class InfrastructureDomainEventHandlersProvider(Provider):
    event_handlers = provide_all(
        UserRegisteredEventHandler,
        scope=Scope.REQUEST
    )
