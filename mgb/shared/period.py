"""
Define the period class.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: Jan 2018
Modified: Jan 2018
"""


class Period(object):
    """Represent a period in time with a begin and an end.

    Time values are expressed as float values, reflecting the simulator approach.
    """

    def __init__(self, begin: float, end: float) -> None:
        """Build a period object.

        :param begin: The period start time.
        :param end: The period end time.
        """
        self._begin = begin
        self._end = end

    @property
    def begin(self) -> float:
        """Define the start time of the period."""
        return self._begin

    @property
    def end(self) -> float:
        """Define the end time of the period."""
        return self._end

    def __add__(self, other: 'Period') -> 'Period':
        """Combine two periods.

        The result period contains the two combined.

        :param other: Second argument to sum.
        :return: Combined period.
        """
        nbegin = min(self.begin, other.begin)
        nend = max(self.end, other.end)
        return Period(nbegin, nend)

    def has_intersection(self, other: 'Period') -> bool:
        """Check if two periods have time intersection.

        :param other: The period to check intersection with.
        :return: If the two periods have time intersection.
        """
        return not (other.end <= self.begin or other.begin >= self.end)

    def __repr__(self) -> str:
        return "Period(begin: {}, end: {})".format(self.begin, self.end)
