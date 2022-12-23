"""A module for marvel comics."""

from attr import dataclass


@dataclass(frozen=True)
class Comic:
    name: str
    n_heroes: int

