"""
Define the contact class.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: Jan 2018
Modified: Jan 2018
"""

import enum

ConnectionType = enum.Enum('ConnectionType', 'DOWN UP')


class Connection(object):
    """Encapsulate a connection information parsed from a trace file in the ONE format.

    A connection information is expected to be in the following format:
        [time] CONN [node1] [node2] [type]
        Ex: 1.00 CONN 28 37 up
    """

    def __init__(self, line: str) -> None:
        """Initialize the connection info with a trace file line information.
        
        :param line: A line extracted from a trace file.
        """
        data = line.split()
        self._time = float(data[0])
        self._node1 = int(data[2])
        self._node2 = int(data[3])
        self._con_type = ConnectionType[data[4].upper()]

    @property
    def time(self) -> float:
        return self._time

    @property
    def node1(self) -> int:
        return self._node1

    @property
    def node2(self) -> int:
        return self._node2

    @property
    def con_type(self) -> ConnectionType:
        return self._con_type

    def __repr__(self) -> str:
        return (f"Connection(time={self.time}, node1={self.node1}, node2={self.node2},"
                f" con_type={self.con_type})")
