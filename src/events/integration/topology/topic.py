from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class Topic:
    """Defines where the events would be sent to or listened from"""
    name: str
