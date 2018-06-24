"""
Define the MergedGroup class.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: Jun 2018
Modified: Jun 2018
"""

from mgb.group_merging import GroupEncounter


class MergedGroup(object):
    """
    Encapsulates the data of merged groups.
    """

    def __init__(self, encounter: GroupEncounter):
        """
        Creates a merged group instance.
        :param encounter: The first encounter to initialize the merged group.
        """
        self.members = encounter.members
        self.periods = [encounter.period]

    def try_merge(self, encounter: GroupEncounter) -> bool:
        """
        Try to merge a group with a new encounter.

        The merge is only executed if the similarity coefficient is greater or equal 0.5.
        :param encounter: The encounter to merge.
        :return: If the merge was executed or not.
        """
        if encounter.get_similarity_coefficient(self.members) >= 0.5:
            self.members.update(encounter.members)
            self.periods.append(encounter.period)
            return True
        return False