"""
This module contains the logic associated with the second step of the algorithm.

In this step the device process all detected groups and combine them based on Group Similarity
Coefficient.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: Jun 2018
Modified: Jun 2018
"""

from mgb.group_merging.group_encounter import GroupEncounter
from mgb.group_merging.merged_group import MergedGroup
from mgb.group_merging.group_merging_runner import GroupMergingRunner