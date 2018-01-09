"""
Define the MobileNeighborhood class.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: Jan 2018
Modified: Jan 2018
"""

from typing import Dict, TypeVar, Set, AbstractSet
from entity import Entity

# Define the types supported for checking with 'in' instruction
MEMBER = TypeVar('MEMBER', int, Entity)


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

    def __getitem__(self, uid: int) -> Entity:
        """Enable access by key."""
        return self.entities[uid]

    def __contains__(self, item: MEMBER) -> bool:
        """Enable in operator."""
        return item in self.entities

    def __repr__(self) -> str:
        return "MobileNeighborhood(entities: {!r})".format(self.entities)

    def __and__(self, other: 'MobileNeighborhood') -> AbstractSet[int]:
        """Return the ids of intersection between two groups.

        :param other: Other group to be compared with.
        """
        return self.entities.keys() & other.entities.keys()

    def __or__(self, other: 'MobileNeighborhood') -> AbstractSet[int]:
        """Return the ids of union members between two groups.

        :param other: Other group to be compared with.
        """
        return self.entities.keys() | other.entities.keys()

    def __len__(self) -> int:
        return len(self._entities)
