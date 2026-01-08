# User registration example

This example implements communication between two `user` and `email` services with domain and integration events using Outbox pattern.

The goal of this app is to give clients ability to register with email and password. After registering user must receive an mail to their email for verification.

<div align="center">
    <img src="./.github/images/project_structure.png" width="90%" alt="Project structure">
</div>

- [How to run](#how-to-run)
- [Integration event bus implementation](#integration-event-bus-implementation)
- [User service](#user-service)
  - [Domain layer](#domain-layer)
  - [Application layer](#application-layer)
  - [Infrastructure](#infrastructure-layer)
  - [Presentation](#presentation-layer)
- [Email service](#email-service)

## How to run

uv is recommended for this project.

0. Clone the repository

1. Create virtual environment and sync all packages

```bash
uv venv
.venv/Scripts/activate or source .venv/bin/activate
uv sync --all-packages
```

a (optional). Run RabbitMQ from `docker-compose.infra.yml` file if needed

```bash
docker compose -f docker-compose-tests.yml up --wait
```

2. Configure .env's for user and email services

Rename `.env.template` files to `.env` and replace value with your own if needed. The values in templates are defaulted for local deployment.

Email service template:

```shell
RMQ_URL=amqp://guest:guest@127.0.0.1:5672
EMAIL_SENDER_ADDRESS=noreply@localhost
EMAIL_SMTP_SERVER_URL=localhost
```

User service template:

```shell
RMQ_URL=amqp://guest:guest@127.0.0.1:5672
SQL_DATABASE_URL=sqlite+aiosqlite:///database.db
```

3. Run services

```bash
python -m user_service.presentation.http
python -m user_service.infrastructure.outbox

python -m email_service
```

## Integration event bus implementation

This application uses RabbitMQ as a durable integration event bus. In [the event bus implementation](/common/src/common/rabbitmq/bus.py), topic represents an exchange, consumer represents a queue and subscribed event types are used as direct routing keys. The resulting topology will look like this.

<div align="center">
    <img src="./.github/images/rmq_topology.png" width="70%" alt="RabbitMQ topology">
</div>

## User service

User service has a Clean Architecture™ structure. At least I tried to.

<div align="center">
    <img src="./.github/images/user_service.png" width="80%" alt="User service scheme">
</div>

### Domain layer

Domain layer contains one domain entity `User`, that contains email and password. `User` has method `initialize()` that initializes a newly created user and produces `UserRegistered` domain event. `UserRepository` interface is used to create, modify and delete stored `User` instances.

### Application layer

Application layer provides an interactor for user registration usecase:

- Create the user with supplied email and password
- Initialize the user
- Handle domain events
- Store the user in the repository

### Infrastructure layer

Infrastructure layer consists of three parts: `persistense`, `outbox` and `event_handlers`.

- Persistence defines SQLAlchemy ORM models and implements `UserRepository` to be used in the `RegisterUserInteractor`
- Outbox provides an at-least-once semantics for sending integration events. First, the event is stored in the DB within the same transaction. Then, the special outbox processor process reads saves events from the DB and sends them to the message broker. This pattern protects us from message loss and data inconsistency, as the service can crash after saving the user but before sending the event or the service can send the event but crash before saving the user.
- Event handlers implements one domain event handler for `UserRegistered` event, that saves an integration event `UserRegisteredV1` to the outbox. This event will later be sent to the subscribers.

### Presentation layer

Presentation layer is the one providing access for external clients. HTTP API is implemented using FastAPI. To register an user, `POST /user/register` endpoint needs to be called. The endpoint handler validates user input and calls the interactor to perform "business" logic.

## Email service

Email service is much simpler in structure. First, the service registers an consumer to receive `UserRegisteredV1` events.

```python
    # Part of __main__.py
    await bus.register(
        IntegrationEventBusRegistration(
            consumer,
            UserServiceTopic,
            consumer.handlers.keys()
        )
    )
```

```python
# The consumer class
class EmailConsumer(EventHandlerConsumer):
    def __init__(
        self,
        sender: EmailSender,
        settings: EmailSettings
    ) -> None:
        handlers: EventHandlerRegistry = {
            UserRegisteredV1: [self.send_registration_email,]
        }
        super().__init__("email", handlers)

        self.sender = sender
        self.settings = settings

    async def send_registration_email(self, event: UserRegisteredV1) -> None:
        content = build_email(
            sender=self.settings.sender_address,
            recipient=event.email
        )
        await self.sender.send_mail(
            sender=self.settings.sender_address,
            recipient=event.email,
            content=content
        )
```

Secondly, on every received event, the service tries to send an email. The actual implementation just sends a log to stdout for simplicity but the code also has `SMTPSender` that you can define it to be the implementation `EmailSender` in `EmailProvider` dishka provider.

```python
class FakeSender(EmailSender):
    async def send_mail(self, sender: str, recipient: str, content: bytes) -> None:
        logger.info(
            f"Tried to send an email to {recipient} from {sender}."
        )
```
