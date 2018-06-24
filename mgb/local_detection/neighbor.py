"""
Define the neighbor class.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: Jan 2018
Modified: Jun 2018
"""


class Neighbor(object):
    """Encapsulate a neighbor tracked by a mobile device."""

    # Class attributes
    INACTIVE_THRESHOLD = 5
    FRIEND_THRESHOLD = 10

    def __init__(self, uid: int, inactive_threshold: int, friend_threshold: int) -> None:
        """Constructor."""
        self._id = uid
        self._close_counter = 0
        self._away_counter = 0
        self._inactive_threshold = inactive_threshold
        self._friend_threshold = friend_threshold

    def increment_close(self) -> None:
        """Increment the close value and reset away value."""
        self._close_counter += 1
        self._away_counter = 0

    def increment_away(self) -> None:
        """Increment the away value and reset close value."""
        self._away_counter += 1
        self._close_counter = 0

    @property
    def close_counter(self) -> int:
        """Define the consecutive number of times the entity is close."""
        return self._close_counter

    @property
    def away_counter(self) -> int:
        """Define the consecutive number of times the entity is away."""
        return self._away_counter

    @property
    def uid(self) -> int:
        """Entity identifier."""
        return self._id

    @property
    def is_friend(self) -> bool:
        """Define if the entity can be considered a friend based on close value."""
        return self.close_counter >= self._friend_threshold

    @property
    def is_active(self) -> bool:
        """Define if the entity is currently active, based on away value."""
        return self.away_counter < self._inactive_threshold

    def __repr__(self) -> str:
        return "Entity(id: {}, close: {}, away: {})".format(
            self.uid, self.close_counter, self.away_counter)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, int):
            return self.uid == other
        elif isinstance(other, type(self)):
            return self.uid == other.uid
        else:
            return False

    def __hash__(self) -> int:
        return self.uid
