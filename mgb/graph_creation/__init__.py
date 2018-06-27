"""
This module contains the logic associated with the fourth step of algorithm (the last one).
In this step we have all detected groups, so we build the group graph used to compute the shortest
path to send messages through.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: Jun 2018
Modified: Jun 2018
"""

from mgb.graph_creation.graph_creation_runner import GraphCreationRunner