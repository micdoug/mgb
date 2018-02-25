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
from mgb import ConnectionGenerator
from mgb import MobileDevice
from mgb import Entity
from typing import List
from pdb import set_trace
import json


@click.command(name="MGB")
@click.option('--trace-file', help="File with contact info, used in the simulation.", 
              required=True)
@click.option('--friend-threshold',
              help="Number of consecutive contacts to consider a node friend.",
              type=int,
              required=True)
@click.option('--inactive-threshold',
              help="Number of failures to consider a node inactive",
              type=int,
              required=True)
@click.option('--number-of-nodes',
              help="Number of nodes to create in the simulation.",
              type=int,
              required=True)
@click.option('--scan-interval',
              type=int,
              help="Number of seconds to wait before running the next step of the detection"
              "algorithm", required=True)
@click.option('--output-file', help="File used to store detected groups.", required=True)
def main(trace_file: str,
         friend_threshold: int,
         inactive_threshold: int,
         number_of_nodes: int,
         scan_interval: float,
         output_file: str) -> None:

    devices: List[MobileDevice] = [MobileDevice(uid) for uid in range(number_of_nodes)]
    Entity.FRIEND_THRESHOLD = friend_threshold
    Entity.INACTIVE_THRESHOLD = inactive_threshold

    period = 1
    with ConnectionGenerator(trace_file, scan_interval) as con_gen:
        while not con_gen.has_finished:
            print(f"Loading connections from period {period}")
            for connection in con_gen:
                if connection.con_type == ConnectionType.UP:
                    devices[connection.node1].add_connection(connection.node2)
                    devices[connection.node2].add_connection(connection.node1)
                elif connection.con_type == ConnectionType.DOWN:
                    devices[connection.node1].remove_connection(connection.node2)
                    devices[connection.node2].remove_connection(connection.node1)
                else:
                    raise RuntimeError("Invalid connection type {connection}")
            print(f"Running local detection algorithm for period {period}")
            for device in devices:
                device.run_local_detection(period*scan_interval)
            period += 1
    # Collect all detected groups to output
    final_result = {
        dev.uid: [{
            "started": mn.started,
            "ended": mn.ended,
            "members": list(mn.entities.keys())
            } for mn in dev.archived] for dev in devices
    }
    print("Writing output file")
    with open(output_file, "w", encoding="utf8") as out_file:
        json.dump(final_result, out_file)
    print(f"{period} periods loaded")