"""
This module contains the logic associated with the fourth step of algorithm (the last one).
In this step we have all detected groups, so we build the group graph used to compute the shortest
path to send messages through.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: Jun 2018
Modified: Jun 2018
"""

from mgb.neighborhood_inspection import MultiMergedGroup
from mgb.shared import Configuration
import logging
from typing import List, Dict
import networkx as nx
from itertools import permutations
from math import exp, log
import pickle
import os.path as path
import json


class GraphCreationRunner(object):

    def __init__(self, config: Configuration):
        self.config = config
        self._logger = logging.getLogger('GraphCreation')

    def run(self, input: Dict[int, List[MultiMergedGroup]]):
        self._logger.info('Starting creating group graphs.')
        simulation_time = self.config.step4_simulation_time
        message_ttl = self.config.step4_message_ttl

        for uid, multi_merged_groups in input.items():
            self._logger.debug(f"Processing device {uid}.")
            self._logger.debug("Creating group identifiers")
            # first we need to generate an identifier for each merged group
            # to represent it as a vertex in the graph
            groups_identified = {
                identifier: group for identifier, group in enumerate(multi_merged_groups)
            }

            # Compute groups weight
            self._logger.debug("Calculating groups' weight.")
            groups_weight = {}
            for group_id, group in groups_identified.items():
                weight = 1 - exp(-(message_ttl * (len(group.periods)/simulation_time)))
                groups_weight[group_id] = weight
                logging.debug(f"Group weight {weight}")

            # Build the graph
            logging.debug(f"Building the graph")
            graph = nx.Graph()
            for group_a_id, group_b_id in permutations(groups_identified, 2):
                group_a = groups_identified[group_a_id]
                group_b = groups_identified[group_b_id]
                group_similarity = len(group_a.members & group_b.members) / len(group_a.members | group_b.members)
                edge_weight = groups_weight[group_a_id] * groups_weight[group_b_id] * group_similarity
                logging.debug(f"Calculating edge ({group_a_id}, {group_b_id}) with weight {edge_weight}")
                if edge_weight == 0:
                    edge_weight = float('inf')
                else:
                    edge_weight = -log(edge_weight)
                graph.add_edge(group_a_id, group_b_id, weight=edge_weight)
                logging.debug(f"Added edge ({group_a_id}, {group_b_id}) with weight {edge_weight}")

            prefix = self.config
            graph_filename = path.join(
                self.config.output_dir,
                f"{self.config.step4_output_prefix}node{uid}.pickle"
            )
            logging.debug(f"Writing file {graph_filename}")
            with open(graph_filename, 'wb') as pickle_output:
                pickle.dump(graph, pickle_output)
            groups_filename = path.join(
                self.config.output_dir,
                f"{self.config.step4_output_prefix}node{uid}.json"
            )
            logging.debug(f"Writing file {groups_filename}")
            with open(groups_filename, 'w', encoding='utf-8') as groups_output:
                output_data = [{
                    "id": identifier,
                    "members": list(group.members),
                    "encounters": [[p.begin, p.end] for p in group.periods]
                } for (identifier, group) in groups_identified.items()]
                json.dump(output_data, groups_output)
