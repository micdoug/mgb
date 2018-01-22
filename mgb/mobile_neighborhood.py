"""
Define the MobileNeighborhood class.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: Jan 2018
Modified: Jan 2018
"""

from typing import Dict, TypeVar, Set, AbstractSet
from mgb.entity import Entity

# Define the types supported for checking with 'in' instruction
MEMBER = TypeVar('MEMBER', int, Entity)

OPERATOR = TypeVar('OPERATOR', Set[int], 'MobileNeighborhood')


class MobileNeighborhood(object):
    """Define a neighborhood set.

    It stores references to entities in the neighborhood.
    """

    def __init__(self) -> None:
        """Initialize internal dictionary."""
        self._entities: Dict[int, Entity] = {}

    @property
    def entities(self) -> Dict[int, Entity]:
        """Access the internal entities representation."""
        return self._entities

    @property
    def is_active(self):
        """Check if the mobile neighborhood is active.

        A group is considered active when at least 50% of the members are active.
        """
        if self:
            not_active = len([m for m in self.entities.values() if not m.is_active])
            return (not_active / len(self)) < 0.5
        else:
            return True

    def add(self, uid: int) -> None:
        """Add a new entity in the neighborhood list.

        :param uid: Entity identifier.
        """
        if uid not in self.entities:
            self.entities[uid] = Entity(uid)

    def remove(self, uid: int) -> None:
        """Remove an entity from the neighborhood list.

        :param id: Entity identifier.
        """
        if uid in self.entities:
            del self.entities[uid]

    def group_correlation(self, other: 'MobileNeighborhood') -> float:
        """Calculate the group correlaction coefficient between two groups.

        The group correlation coefficient is defined as the number of members in the intersection
        of the two groups divided by the number of members in the union of the two groups.

        :param other: The other group to compare with.
        """
        if not self or not other:
            return 0
        else:
            return len(self & other) / len(self | other)

    def __getitem__(self, uid: int) -> Entity:
        """Enable access by key."""
        return self.entities[uid]

    def __contains__(self, item: MEMBER) -> bool:
        """Enable in operator."""
        return item in self.entities

    def __repr__(self) -> str:
        return "MobileNeighborhood(entities: {!r})".format(self.entities)

    def __and__(self, other: OPERATOR) -> AbstractSet[int]:
        """Return the ids of intersection between two groups.

        :param other: Other group to be compared with or a set of ids.
        """
        if isinstance(other, set):
            return self._entities.keys() & other
        else:
            return self.entities.keys() & other.entities.keys()

    def __or__(self, other: OPERATOR) -> AbstractSet[int]:
        """Return the ids of union members between two groups.

        :param other: Other group to be compared with.
        """
        if isinstance(other, set):
            return self._entities.keys() | other
        else:
            return self.entities.keys() | other.entities.keys()

    def __sub__(self, other: OPERATOR) -> AbstractSet[int]:
        if isinstance(other, set):
            return self._entities.keys() - other
        else:
            return self._entities.keys - other._entities.keys()

    def __rsub__(self, other: OPERATOR) -> AbstractSet[int]:
        if isinstance(other, set):
            return other - self._entities.keys()
        else:
            return other._entities.keys() - self._entities.keys

    def __len__(self) -> int:
        return len(self._entities)
