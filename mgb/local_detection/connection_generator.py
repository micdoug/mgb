"""
Define the class ConnectionGenerator that encapsulates the logic of read connections from a file
according to the scan interval used.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: Feb 2018
Modified: Feb 2018
"""

from typing import Generator, Optional
from mgb.local_detection import Connection


class ConnectionGenerator(object):
    """Create a generator to load connections from the external file."""

    def __init__(self, input_file: str, scan_interval: float) -> None:
        self._input_file_path = input_file
        self._scan_interval = scan_interval
        self._cached = None
        self._limit_time: float = 0
        self._has_finished = False
        self._counter = 0

    @property
    def has_finished(self) -> bool:
        """Check if the generator has parsed the file until the end."""
        return self._has_finished

    def __enter__(self) -> 'ConnectionGenerator':
        """When starting the scope the input file is opened."""
        self._input_file = open(self._input_file_path, "r", encoding="utf8")
        return self

    def __exit__(self, *args) -> None:
        """When exiting the scope the input file is closed."""
        self._input_file.close()

    def __next__(self) -> Connection:
        """Define the logic of reading connections from the file."""
        self._counter += 1

        if self._cached:
            if self._cached.time <= self._limit_time:
                cached = self._cached
                self._cached = None
                return cached
            else:
                raise StopIteration()

        line = self._input_file.readline()
        if not line:
            self._has_finished = True
            raise StopIteration()

        connection = Connection(line)
        if connection.time <= self._limit_time:
            return connection
        else:
            self._cached = connection
            raise StopIteration()

    def __iter__(self) -> Optional['ConnectionGenerator']:
        """Return itself as an iterator."""
        if self._input_file or self._cached:
            self._limit_time += self._scan_interval
            return self
        else:
            return None
