"""
Define the LocalDetectionRunner class.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: Jun 2018
Modified: Jun 2018
"""
from mgb.local_detection import Neighborhood, ConnectionGenerator, ConnectionType
from mgb.shared import Configuration
from typing import Dict, List
import logging
from mgb.local_detection import Device
import os.path as path
import json


class LocalDetectionRunner(object):

    def __init__(self, config: Configuration):
        """
        Creates a new runner.
        :param config: The current configuration.
        """
        self._config = config
        self._logger = logging.getLogger("LocalDetection")

    def run(self) -> Dict[int, List[Neighborhood]]:
        """
        Executes the local detection step.
        :return: A dictionary with each device found neighborhood.
        """
        self._logger.info("Starting the 'Local Detection' step.")
        number_of_nodes = self._config.nrof_nodes
        self._logger.info(f"Creating {self._config.nrof_nodes} nodes.")
        self._logger.info(f"Calibrating friend threshold to {self._config.friend_threshold}")
        self._logger.info(f"Calibrating inactive threshold to {self._config.inactive_threshold}")
        devices = [Device(uid, self._config) for uid in range(number_of_nodes)]

        period = 1
        scan_interval = self._config.scan_interval
        log = f"Starting contact simulation considering a scan interval of {scan_interval} seconds"
        self._logger.info(log)
        trace_file = self._config.trace_file

        # Ensuring that the trace file exists
        if not path.exists(trace_file):
            raise RuntimeError(f"The trace file {trace_file} does not exists.")

        with ConnectionGenerator(trace_file, scan_interval) as con_gen:
            while not con_gen.has_finished:
                self._logger.debug(f"Loading connections from period {period}.")
                for connection in con_gen:
                    if connection.con_type == ConnectionType.UP:
                        devices[connection.node1].add_connection(connection.node2)
                        devices[connection.node2].add_connection(connection.node1)
                    elif connection.con_type == ConnectionType.DOWN:
                        devices[connection.node1].remove_connection(connection.node2)
                        devices[connection.node2].remove_connection(connection.node1)
                    else:
                        raise RuntimeError(f"Invalid connection type {connection}.")
                self._logger.debug(f"Running local detection algorithm for period {period}")
                for device in devices:
                    device.run_local_detection(period*scan_interval)
                period += 1

        self._logger.debug(f"Processed {period} periods of {scan_interval} seconds.")
        self._logger.info("Formatting output data.")
        result = {device.uid: device.archived for device in devices}

        if not self._config.step1_enable_output:
            return result

        prefix = self._config.step1_output_prefix
        self._logger.debug(f"Using output prefix {prefix}")
        enable_filter = self._config.step1_enable_filtering
        self._logger.debug(f"Using filter: {enable_filter}")
        size_threshold = self._config.step1_size_threshold
        self._logger.debug(f"Using size threshold of {size_threshold}")

        self._logger.info(f"Writing output")
        for device in devices:
            filename = path.join(self._config.output_dir, f"{prefix}node{device.uid}.json")
            if enable_filter:
                output_data = [{
                    "started": mn.started,
                    "ended": mn.ended,
                    "members": list(mn.entities)
                } for mn in device.archived if len(mn.entities) >= size_threshold]
            else:
                output_data = [{
                    "started": mn.started,
                    "ended": mn.ended,
                    "members": list(mn.entities)
                } for mn in device.archived]
            self._logger.debug(f"Writing output {filename}")
            with open(filename, 'w', encoding='utf-8') as output:
                json.dump(output_data, output)

        return result