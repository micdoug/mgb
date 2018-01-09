"""
Define the MobileDevice class.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: Jan 2018
Modified: Jan 2018
"""

from typing import Set
from mobile_neighborhood import MobileNeighborhood


class MobileDevice(object):
    """Define a mobile device.

    A mobile device keep track of its neighboohood and execute the local detection part
    of the algorithm.
    """

    def __init__(self, uid: int) -> None:
        self._uid = uid
        self.reset_strangers()
        self.reset_friends()

    def _reset_strangers(self) -> None:
        self._strangers = MobileNeighborhood()
    
    def _reset_friends(self) -> None:
        self._friends = MobileNeighborhood()


    @property
    def uid(self) -> int:
        """Return the mobile unique identifier."""
        return self._uid

    