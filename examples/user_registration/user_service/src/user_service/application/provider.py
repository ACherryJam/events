from typing import Iterable
from dishka import Provider, Scope, provide_all
from events.domain.implementation.dishka import DomainEventImplementationProvider

from user_service.application.user.register_user import RegisterUserInteractor


class InteractorsProvider(Provider):
    interactors = provide_all(
        RegisterUserInteractor,
        scope=Scope.REQUEST
    )


def get_application_providers() -> Iterable[Provider]:
    return [
        InteractorsProvider(),
        DomainEventImplementationProvider(),
    ]
