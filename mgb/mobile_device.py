"""
Define the MobileDevice class.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: Jan 2018
Modified: Jan 2018
"""

from typing import Set, List
from mgb.mobile_neighborhood import MobileNeighborhood


class MobileDevice(object):
    """Define a mobile device.

    A mobile device keep track of its neighboohood and execute the local detection part
    of the algorithm.
    """

    def __init__(self, uid: int) -> None:
        """Initialize mobile device data.

        :param uid: Identifier of the mobile device.
        """
        self._uid = uid
        self._current_connections: Set[int] = set()
        self._strangers = MobileNeighborhood()
        self._friends = MobileNeighborhood()
        self._archived: List[Set[int]] = []

    def add_connection(self, uid: int) -> None:
        """Add a new connection in the list.

        :param uid: Identifier of the other node in the connection.
        """
        self._current_connections.add(uid)

    def remove_connection(self, uid: int) -> None:
        """Remove a connection from the list.

        :param uid: Identifier of the other node in the connection.
        """
        self._current_connections.remove(uid)

    def _reset_strangers(self) -> None:
        """Reset current strangers."""
        self._strangers = MobileNeighborhood()

    def _reset_friends(self) -> None:
        """Reset current friends."""
        self._friends = MobileNeighborhood()

    @property
    def uid(self) -> int:
        """Return the mobile unique identifier."""
        return self._uid

    @property
    def archived(self) -> List[Set[int]]:
        """Access archived friends lists (groups)."""
        return self._archived

    @property
    def friends(self) -> MobileNeighborhood:
        return self._friends

    @property
    def strangers(self) -> MobileNeighborhood:
        return self._strangers

    def run_local_detection(self) -> None:
        """Run the local detection algorithm based on current state."""
        self._update_friends_connection()
        self._update_strangers_connection()

        # Check if we need to archive current friend list as a group
        if not self._friends.is_active:
            uids = set(self.friends._entities.keys())
            uids.add(self.uid)
            if len(uids) > 2:
                self._archived.append(uids)
            self._friends = MobileNeighborhood()
            self._strangers = MobileNeighborhood()

    def _update_friends_connection(self) -> None:
        """Update friends information based on current connections.

        An entity in the friends list has its close_counter incremented if there are
        a connection with it. Otherwise, it has its away_counter incremented.
        """
        # Friend with current connection
        for uid in (self._friends & self._current_connections):
            self._friends[uid].increment_close()

        # Friends without current connection
        for uid in (self._friends - self._current_connections):
            self._friends[uid].increment_away()

    def _update_strangers_connection(self) -> None:
        """Update strangers information based on current connections.

        An entity in the strangers list has its close_counter incremented if there are a
        connection with it. If there are no connection with it, the away counter is incremented.
        New nodes are added in the strangers list. Nodes with a number of connections greater
        than the threshold, are transferred to friends list.
        """
        # Strangers without current connection
        for uid in (self._strangers - self._current_connections):
            self._strangers[uid].increment_away()
            # If the entity is inactive, remove it from strangers list
            if not self._strangers[uid].is_active:
                self._strangers.remove(uid)

        # Strangers with current connection
        for uid in (self._strangers & self._current_connections):
            self._strangers[uid].increment_close()
            # If the entity is a friend, remove it from strangers list and add it to friends
            if self._strangers[uid].is_friend:
                self._strangers.remove(uid)
                self._friends.add(uid)

        # New strangers
        for uid in (self._current_connections - (self._strangers | self._friends)):
            self._strangers.add(uid)
            self._strangers[uid].increment_close()
