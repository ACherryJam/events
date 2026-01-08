from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from events.domain.implementation.dishka.provider import DomainEventImplementationProvider

from user_service.application.provider import get_application_providers
from user_service.infrastructure.provider import get_infrastructure_providers
from user_service.infrastructure.persistence.settings import SQLPersistenceSettings

from .features.user import user_router
from .features.health import health_router


def create_container() -> AsyncContainer:
    return make_async_container(
        DomainEventImplementationProvider(),
        *get_application_providers(),
        *get_infrastructure_providers(),
        context={
            SQLPersistenceSettings: SQLPersistenceSettings(),
        }
    )



@asynccontextmanager
async def lifespan(app: FastAPI):
    container = app.state.dishka_container

    yield

    await container.close()


def create_app() -> FastAPI:
    container = create_container()

    app = FastAPI(
        lifespan=lifespan
    )
    setup_dishka(container, app=app)

    app.include_router(user_router)
    app.include_router(health_router)

    return app


if __name__ == "__main__":
    uvicorn.run(
        create_app(),
        host="0.0.0.0",
        port=8000
    )
