from dataclasses import dataclass


@dataclass
class Message:
    username: str
    message: str
