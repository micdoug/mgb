"""
Define the GroupMergingRunner class.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: Jun 2018
Modified: Jun 2018
"""

from mgb.shared import Configuration
from typing import Dict, List
from mgb.local_detection import Neighborhood
from mgb.group_merging import GroupEncounter, MergedGroup
import logging
import os.path as path
import json


class GroupMergingRunner(object):
    """
    This class encapsulates the running logic of the second step of the algorithm.
    """

    def __init__(self, config: Configuration, ):
        self.config = config
        self._logger = logging.getLogger('GroupMerging')

    def run(self, input: Dict[int, List[Neighborhood]]) -> Dict[int, List[MergedGroup]]:
        """
        Execute the merging group step.
        :param input: The groups detected by each device in the previous step.
        :return: Merged groups for each device.
        """
        self._logger.info("Starting merging groups.")
        merged_by_device = {}

        for uid, neighborhood_list in input.items():
            self._logger.debug(f"Merging groups of device {uid}")
            if not neighborhood_list:
                merged_by_device[uid] = []
                continue

            encounters = [
                GroupEncounter(set(neighborhood.entities), neighborhood.started, neighborhood.ended)
                for neighborhood in neighborhood_list
            ]
            first_encounter = encounters.pop(0)
            merged_groups = [MergedGroup(first_encounter)]
            for encounter in encounters:
                has_merged = False
                for merged_group in merged_groups:
                    if merged_group.try_merge(encounter):
                        has_merged = True
                        break
                if not has_merged:
                    merged_groups.append(MergedGroup(encounter))

            merged_by_device[uid] = merged_groups
            if self.config.step2_enable_filtering:
                self._logger.debug(f"Filtering merged groups for device {uid}")
                merged_by_device[uid] = [
                    mg for mg in merged_groups
                    if len(mg.periods) >= self.config.step2_encounters_threshold
                ]
            self._logger.debug(f"Found {len(merged_by_device[uid])} merged groups for device {uid}")

        if not self.config.step2_enable_output:
            return merged_by_device

        self._logger.info("Writing output")
        for uid, merged_groups in merged_by_device.items():
            filename = path.join(
                self.config.output_dir,
                f"{self.config.step2_output_prefix}node{uid}.json"
            )
            output_data = [{
                "members": list(mgroup.members),
                "encounters": [[p.begin, p.end] for p in mgroup.periods]
            } for mgroup in merged_groups]
            self._logger.debug(f"Writing output {filename}")
            with open(filename, 'w', encoding='utf-8') as output:
                json.dump(output_data, output)

        return merged_by_device