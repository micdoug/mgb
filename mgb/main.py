"""
Program entry point.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: Jan 2018
Modified: Feb 2018
"""

import click
from mgb import MobileDevice
from mgb import Connection, ConnectionType
from mgb import Configuration
from mgb import ConnectionGenerator
from mgb import MobileDevice
from mgb import Entity
from typing import List
import json
import logging


@click.command(name="MGB")
@click.argument('configuration_file', required=True)
@click.option('--verbose/--no-verbose', help="Enable more debug messages.", default=False)
def main(configuration_file: str,
         verbose: bool) -> None:

    if verbose:
        logging.basicConfig(level="DEBUG")
    else:
        logging.basicConfig(level="INFO")

    logging.debug('Loading configuration file')
    try:
        config = Configuration(configuration_file)
    except Exception as e:
        logging.error(f'Error on loading configuration file "{configuration_file}"')
        logging.error(e)
        exit(1)

    print(vars(config))

    # devices: List[MobileDevice] = [MobileDevice(uid) for uid in range(number_of_nodes)]
    # Entity.FRIEND_THRESHOLD = friend_threshold
    # Entity.INACTIVE_THRESHOLD = inactive_threshold
    #
    # period = 1
    # logging.info("Starting detection algorithm")
    # logging.info(f"Setting friend threshold to {Entity.FRIEND_THRESHOLD}")
    # logging.info(f"Setting inactive threshold to {Entity.INACTIVE_THRESHOLD}")
    # logging.info(f"Starting processing contacts with interval of {scan_interval} seconds")
    # with ConnectionGenerator(trace_file, scan_interval) as con_gen:
    #     while not con_gen.has_finished:
    #         logging.debug(f"Loading connections from period {period}")
    #         for connection in con_gen:
    #             if connection.con_type == ConnectionType.UP:
    #                 devices[connection.node1].add_connection(connection.node2)
    #                 devices[connection.node2].add_connection(connection.node1)
    #             elif connection.con_type == ConnectionType.DOWN:
    #                 devices[connection.node1].remove_connection(connection.node2)
    #                 devices[connection.node2].remove_connection(connection.node1)
    #             else:
    #                 raise RuntimeError("Invalid connection type {connection}")
    #         logging.debug(f"Running local detection algorithm for period {period}")
    #         for device in devices:
    #             device.run_local_detection(period*scan_interval)
    #         period += 1
    # # Collect all detected groups to output
    # final_result = {
    #     dev.uid: [{
    #         "started": mn.started,
    #         "ended": mn.ended,
    #         "members": list(mn.entities.keys())
    #         } for mn in dev.archived] for dev in devices
    # }
    # logging.info("Writing output file")
    # with open(output_file, "w", encoding="utf8") as out_file:
    #     json.dump(final_result, out_file)
    # logging.info(f"Processed {period} periods of {scan_interval} seconds")