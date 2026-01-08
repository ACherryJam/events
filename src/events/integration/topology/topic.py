from dataclasses import dataclass


@dataclass
class Topic:
    """Defines where the events would be sent to or listened from"""
    name: str
