"""
Defines the GroupEncounter class.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: Jun 2018
Modified: Jun 2018
"""

from typing import Set
from mgb.shared import Period


class GroupEncounter(object):
    """
    Encapsulates information of a group encounter.
    """

    def __init__(self, members: Set[int], start: float, end: float):
        """
        Create a new group encounter.
        :param members: The members present in the encounter.
        :param start: The encounter start time.
        :param end: The encounter end time.
        """
        self.period = Period(start, end)
        self.members = members

    def get_similarity_coefficient(self, devices: Set[int]) -> float:
        """
        Return the group similarity considering internal members and a given devices set.
        :param devices: The devices set to check similarity with.
        :return: The similarity coefficient (varies from 0 to 1.0).
        """
        # safe guard for division by zero
        if not (self.members or devices):
            return 0.0

        return len(self.members & devices) / len(self.members | devices)
