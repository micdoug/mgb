"""
Define the NeighborhoodIntrospectionRunner

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: May 2018
Modified: May 2018
"""

from mgb.shared import Configuration
from typing import Dict, List
from mgb.group_merging import MergedGroup
import logging
from copy import deepcopy
from mgb.neighborhood_inspection import MultiMergedGroup
import os.path as path
import json


class NeighborhoodInspectionRunner(object):

    def __init__(self, config: Configuration):
        self.config = config
        self._logger = logging.getLogger('NeighborhoodInspection')

    def run(self, input: Dict[int, List[MergedGroup]]) -> Dict[int, List[MergedGroup]]:
        self._logger.info('Starting neighborhood inspection step')

        # Since we are merging information across mutable objects we need to create a shadow copy
        # to ensure consistency. Oh god \o/
        shadow_input = deepcopy(input)

        multi_merged_groups_by_device = {}
        for uid, merged_groups in shadow_input.items():
            if not merged_groups:
                multi_merged_groups_by_device[uid] = []
                continue

            multi_merged_groups = [MultiMergedGroup(mg) for mg in merged_groups]
            self._logger.debug(f"Starting processing node {uid}")
            neighbors = set()
            # Fetch all direct neighbors of the current device
            for merged_group in merged_groups:
                neighbors.update(merged_group.members)

            # for each neighbor we need to try to merge its merged groups into the current device
            for neighbor in neighbors:
                for merged_group in input[neighbor]:
                    # prepare yourselves, here we go
                    has_merged = False
                    for multi_merged_group in multi_merged_groups:
                        if multi_merged_group.try_merge(merged_group):
                            has_merged = True
                            break
                    if not has_merged:
                        multi_merged_groups.append(MultiMergedGroup(deepcopy(merged_group)))
            multi_merged_groups_by_device[uid] = multi_merged_groups
            self._logger.debug(f"Found a total of {len(multi_merged_groups)} for device {uid}")

        if self.config.step3_enable_filtering:
            size_threshold = self.config.step3_size_threshold
            encounters_threshold = self.config.step3_encounters_threshold
            for uid, multi_merged_groups in multi_merged_groups_by_device.items():
                self._logger.debug(f"Filtering groups of device {uid}")
                multi_merged_groups_by_device[uid] = [
                    mmg for mmg in multi_merged_groups
                    if len(mmg.members) >= size_threshold
                       and len(mmg.periods) >= encounters_threshold
                ]

        if not self.config.step3_enable_output:
            return multi_merged_groups_by_device

        self._logger.info("Writing output")
        for uid, multi_merged_groups in multi_merged_groups_by_device.items():
            self._logger.debug(f"Writing output of device {uid}")
            filename = path.join(
                self.config.output_dir,
                f"{self.config.step3_output_prefix}node{uid}.json"
            )
            output_data = [{
                "members": list(mmg.members),
                "encounters": [[p.begin, p.end] for p in mmg.periods]
            } for mmg in multi_merged_groups]
            with open(filename, 'w', encoding='utf-8') as output:
                json.dump(output_data, output)

        return multi_merged_groups_by_device

