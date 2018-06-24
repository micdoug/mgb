"""
This module contains the logic associated with the first step of algorithm.
In this step each device runs a local detection algorithm, and defines its own set of groups.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: May 2018
Modified: May 2018
"""

from mgb.local_detection.neighbor import Neighbor
from mgb.local_detection.neighborhood import Neighborhood
from mgb.local_detection.device import Device
from mgb.local_detection.connection import Connection, ConnectionType
from mgb.local_detection.connection_generator import ConnectionGenerator
from mgb.local_detection.local_detection_runner import LocalDetectionRunner
