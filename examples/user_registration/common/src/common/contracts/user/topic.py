from typing import Literal
from events.integration.topology import Topic


_user_service: Literal["users"] = "users"
UserServiceTopic = Topic(_user_service)
