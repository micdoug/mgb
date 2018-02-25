"""
Define the MobileNeighborhood class.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: Jan 2018
Modified: Jan 2018
"""

from typing import Dict, Union, Set, AbstractSet
from mgb.entity import Entity


class MobileNeighborhood(object):
    """Define a neighborhood set.

    It stores references to entities in the neighborhood.
    """

    def __init__(self) -> None:
        """Initialize internal dictionary."""
        self._entities: Dict[int, Entity] = {}
        self._started: float = 0
        self._ended: float = 0

    @property
    def started(self) -> float:
        """Define the time the group was initialized."""
        return self._started

    @property
    def ended(self) -> float:
        """Define the time the group was archived."""
        return self._ended

    @ended.setter
    def ended(self, value: float) -> None:
        """Set the time the group was archived.

        :param value: The value to set.
        """
        assert value >= self.started
        self._ended = value

    @property
    def entities(self) -> Dict[int, Entity]:
        """Access the internal entities representation."""
        return self._entities

    @property
    def is_active(self) -> bool:
        """Check if the mobile neighborhood is active.

        A group is considered active when at least 50% of the members are active.
        """
        if self:
            not_active = len([m for m in self.entities.values() if not m.is_active])
            return (not_active / len(self)) < 0.5
        else:
            return True

    def add(self, uid: int, time: float) -> None:
        """Add a new entity in the neighborhood list.

        :param uid: Entity identifier.
        :param time: Current simulation time.
        """
        if not self.entities:
            self._started = time
        if uid not in self.entities:
            self.entities[uid] = Entity(uid)
            self._ended = time

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

    def __contains__(self, item: Union[int, Entity]) -> bool:
        """Enable in operator."""
        return item in self.entities

    def __repr__(self) -> str:
        return "MobileNeighborhood(entities: {!r})".format(self.entities)

    def __and__(self, other: Union['MobileNeighborhood', Set[int]]) -> AbstractSet[int]:
        """Return the ids of intersection between two groups.

        :param other: Other group to be compared with or a set of ids.
        """
        if isinstance(other, set):
            return self._entities.keys() & other
        else:
            return self.entities.keys() & other.entities.keys()

    def __or__(self, other: Union['MobileNeighborhood', Set[int]]) -> AbstractSet[int]:
        """Return the ids of union members between two groups.

        :param other: Other group to be compared with.
        """
        if isinstance(other, set):
            return self._entities.keys() | other
        else:
            return self.entities.keys() | other.entities.keys()

    def __sub__(self, other: Union['MobileNeighborhood', Set[int]]) -> AbstractSet[int]:
        if isinstance(other, set):
            return self._entities.keys() - other
        else:
            return self._entities.keys() - other._entities.keys()

    def __rsub__(self, other: 'MobileNeighborhood') -> AbstractSet[int]:
        if isinstance(other, set):
            return other - self.entities.keys()
        else:
            return other._entities.keys() - self.entities.keys()

    def __len__(self) -> int:
        return len(self._entities)
