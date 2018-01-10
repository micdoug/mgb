"""
Define the MobileDevice class unit tests.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: Jan 2018
Modified: Jan 2018
"""

from unittest import TestCase
from mobile_device import MobileDevice
from entity import Entity
from nose.tools import set_trace


class MobileDeviceTests(TestCase):
    """MobileDevice unit tests."""

    def test_constructor(self):
        """Test initialization."""
        device = MobileDevice(1)
        self.assertEqual(device.uid, 1)
        self.assertFalse(device.archived)
        self.assertFalse(device.strangers)
        self.assertFalse(device.friends)

    def test_basic_detection(self):
        """Test a sequence of connections."""
        device = MobileDevice(1)
        Entity.FRIEND_THRESHOLD = 3
        Entity.INACTIVE_THRESHOLD = 2
        
        # Add connection with 2 and 3, they should be included in strangers list
        device.add_connection(2)
        device.add_connection(3)
        device.run_local_detection()
        self.assertEqual(len(device.friends), 0)
        self.assertEqual(len(device.strangers), 2)
        self.assertIn(2, device.strangers)
        self.assertEqual(device.strangers[2].close_counter, 1)
        self.assertIn(3, device.strangers)
        self.assertEqual(device.strangers[3].close_counter, 1)

        # Scan again
        device.run_local_detection()
        self.assertEqual(len(device.friends), 0)
        self.assertEqual(len(device.strangers), 2)
        self.assertIn(2, device.strangers)
        self.assertEqual(device.strangers[2].close_counter, 2)
        self.assertIn(3, device.strangers)
        self.assertEqual(device.strangers[3].close_counter, 2)

        # Remove connection with 3 and scan again
        device.remove_connection(3)
        device.run_local_detection()
        self.assertEqual(len(device.friends), 1)
        self.assertEqual(len(device.strangers), 1)
        self.assertIn(2, device.friends)
        self.assertEqual(device.friends[2].close_counter, 0)
        self.assertEqual(device.friends[2].away_counter, 0)
        self.assertIn(3, device.strangers)
        self.assertEqual(device.strangers[3].close_counter, 0)
        self.assertEqual(device.strangers[3].away_counter, 1)

        # Add connection with 4
        device.add_connection(4)
        device.run_local_detection()
        self.assertEqual(len(device.friends), 1)
        self.assertEqual(len(device.strangers), 1)
        self.assertIn(2, device.friends)
        self.assertEqual(device.friends[2].close_counter, 1)
        self.assertEqual(device.friends[2].away_counter, 0)
        self.assertNotIn(3, device.strangers)
        self.assertIn(4, device.strangers)
        self.assertEqual(device.strangers[4].close_counter, 1)
        self.assertEqual(device.strangers[4].away_counter, 0)

        # Run scan twice to add 4 in the friends list
        device.run_local_detection()
        device.run_local_detection()
        self.assertEqual(len(device.friends), 2)
        self.assertEqual(len(device.strangers), 0)
        self.assertIn(2, device.friends)
        self.assertEqual(device.friends[2].close_counter, 3)
        self.assertEqual(device.friends[2].away_counter, 0)
        self.assertIn(4, device.friends)
        self.assertEqual(device.friends[4].close_counter, 0)
        self.assertEqual(device.friends[4].away_counter, 0)

        # Lost connection with 2 and 4
        device.remove_connection(2)
        device.remove_connection(4)
        device.add_connection(3)
        device.run_local_detection()
        self.assertEqual(len(device.friends), 2)
        self.assertEqual(len(device.strangers), 1)
        self.assertIn(2, device.friends)
        self.assertEqual(device.friends[2].close_counter, 0)
        self.assertEqual(device.friends[2].away_counter, 1)
        self.assertIn(4, device.friends)
        self.assertEqual(device.friends[4].close_counter, 0)
        self.assertEqual(device.friends[4].away_counter, 1)
        self.assertIn(3, device.strangers)
        self.assertEqual(device.strangers[3].close_counter, 1)
        self.assertEqual(device.strangers[3].away_counter, 0)

        # Run scan again, should archive friends
        device.run_local_detection()
        self.assertEqual(len(device.friends), 0)
        self.assertEqual(len(device.strangers), 0)
        self.assertEqual(len(device.archived), 1)
        self.assertIn(1, device.archived[0])
        self.assertIn(2, device.archived[0])
        self.assertNotIn(3, device.archived[0])
        self.assertIn(4, device.archived[0])
