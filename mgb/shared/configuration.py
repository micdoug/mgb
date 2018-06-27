"""
Define the configuration class.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: May 2018
Modified: May 2018
"""

from configparser import ConfigParser


class Configuration(object):
    """Is a container of program configuration data."""

    def __init__(self, file_path: str) -> None:
        """
        Constructor.
        :param file_path: The file to load configuration data from.
        """
        with open(file_path, 'r', encoding='utf8') as input:
            parser = ConfigParser()
            parser.read_file(input)

        # basic section
        self.trace_file = parser.get('basic', 'trace_file')
        self.friend_threshold = parser.getint('basic', 'friend_threshold')
        self.inactive_threshold = parser.getint('basic', 'inactive_threshold')
        self.scan_interval = parser.getint('basic', 'scan_interval')
        self.output_dir = parser.get('basic', 'output_dir')
        self.nrof_nodes = parser.getint('basic', 'nrof_nodes')
        self.scan_interval = parser.getint('basic', 'scan_interval')
        self.output_dir = parser.get('basic', 'output_dir')

        # step1 section
        self.step1_enable_output = parser.getboolean('step1', 'enable_output')
        self.step1_output_prefix = parser.get('step1', 'output_prefix')
        self.step1_enable_filtering = parser.get('step1', 'enable_filtering')
        self.step1_size_threshold = parser.getint('step1', 'size_threshold')

        # step 2 section
        self.step2_enable_output = parser.getboolean('step2', 'enable_output')
        self.step2_output_prefix = parser.get('step2', 'output_prefix')
        self.step2_enable_filtering = parser.getboolean('step2', 'enable_filtering')
        self.step2_encounters_threshold = parser.getint('step2', 'encounters_threshold')

        # step 3 section
        self.step3_enable_output = parser.getboolean('step3', 'enable_output')
        self.step3_output_prefix = parser.get('step3', 'output_prefix')
        self.step3_enable_filtering = parser.getboolean('step3', 'enable_filtering')
        self.step3_size_threshold = parser.getint('step3', 'size_threshold')
        self.step3_encounters_threshold = parser.getint('step3', 'encounters_threshold')

        # step 4 section
        self.step4_output_prefix = parser.get('step4', 'output_prefix')
        self.step4_simulation_time = parser.getint('step4', 'simulation_time')
        self.step4_message_ttl = parser.getint('step4', 'message_ttl')