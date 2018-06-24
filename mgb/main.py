"""
Program entry point.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: Jan 2018
Modified: Feb 2018
"""

import click
from mgb.local_detection import LocalDetectionRunner
from mgb.group_merging import GroupMergingRunner
from mgb.shared import Configuration
import logging
import os.path as path
import os


@click.command(name="MGB")
@click.argument('configuration_file', required=True)
@click.option('--verbose/--no-verbose', help="Enable more debug messages.", default=False)
def main(configuration_file: str,
         verbose: bool) -> None:

    logformat = "%(asctime)s: %(levelname)s [%(name)s]:  %(message)s"
    if verbose:
        logging.basicConfig(level="DEBUG", format=logformat)
    else:
        logging.basicConfig(level="INFO", format=logformat)


    logging.debug('Loading configuration file')
    try:
        config = Configuration(configuration_file)
    except Exception as e:
        logging.error(f'Error on loading configuration file "{configuration_file}"')
        logging.error(e)
        exit(1)

    try:
        os.makedirs(config.output_dir, exist_ok=True)
    except Exception as e:
        logging.exception(e)
        exit(1)

    try:
        local_detection_runner = LocalDetectionRunner(config)
        result = local_detection_runner.run()
    except Exception as e:
        logging.exception(e)
        exit(1)

    try:
        group_merging_runner = GroupMergingRunner(config)
        result = group_merging_runner.run(result)
    except Exception as e:
        logging.exception(e)
        exit(2)
