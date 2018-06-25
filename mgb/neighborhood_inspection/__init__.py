"""
This module contains the logic associated with the third step of algorithm.
In this step each device inspects its neighbors merged groups and combine them with its local
data to build a graph in the next step.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: May 2018
Modified: May 2018
"""

from mgb.neighborhood_inspection.multi_merged_group import MultiMergedGroup
from mgb.neighborhood_inspection.neighborhood_inspection_runner import NeighborhoodInspectionRunner