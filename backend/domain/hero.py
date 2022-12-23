"""A module for marvel heroes."""

from attr import dataclass


@dataclass(frozen=True, repr=True, eq=False, hash=False)
class Collaboration:
    hero1: str
    hero2: str
    n_collabs: int

    def __eq__(self, other):
        if self is other:
            return True

        if (self.hero1 == other.hero1 and self.hero2 == other.hero2) or \
                (self.hero1 == other.hero2 and self.hero2 == other.hero1) or \
                (self.hero2 == other.hero1 and self.hero1 == other.hero2):
            if self.n_collabs == other.n_collabs:
                return True

        return False

    def __hash__(self):
        heroes = ''.join(sorted([self.hero1, self.hero2, str(self.n_collabs)]))
        return hash(heroes)
