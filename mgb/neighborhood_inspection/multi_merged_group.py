"""
Define the MultiMergedGroup class.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: May 2018
Modified: May 2018
"""

from mgb.group_merging import MergedGroup


class MultiMergedGroup(object):
    """
    Encapsulates the operation of merging groups created from a merging operation.

    It handles multiple levels of merging.
    """

    def __init__(self, first_group: MergedGroup):
        """
        Creates a new multi merged group.
        :param first_group: The group used to initialize members and encounters.
        """
        self.members = set(first_group.members)
        self.periods = list(first_group.periods)

    def _get_group_similarity(self, other: MergedGroup) -> float:
        """
        Calculates the group similarity.
        :param other: The other group.
        :return: The group similarity coefficient (varies from 0 to 1.0).
        """
        # safe guard for division by zero
        if not (self.members or other.members):
            return 0
        # intersection / union
        return len(self.members & other.members) / len(self.members | other.members)

    def try_merge(self, other: MergedGroup) -> bool:
        """
        Try to merge a new group.
        :param other: The group to merge.
        :return: If it was possible to merge the new group.
        """
        if self._get_group_similarity(other) >= 0.5:
            self.members.update(other.members)
            # periods must be merged one by one to ensure time cohesion
            for new_period in other.periods:
                has_merged = False
                for period in self.periods:
                    if period.try_merge(new_period):
                        has_merged = True
                        break
                if not has_merged:
                    self.periods.append(new_period)
            return True
        return False
