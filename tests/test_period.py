"""
Unit tests of Period class.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: Jan 2018
Modified: Jan 2018
"""

from unittest import TestCase
from mgb.period import Period


class PeriodTests(TestCase):
    """Period class unit tests."""

    def test_attributes(self):
        """Test internal attributes."""
        # Check value initialization
        period = Period(15, 75)
        self.assertEqual(period.begin, 15)
        self.assertEqual(period.end, 75)

        # Check readonly properties
        with self.assertRaises(AttributeError):
            period.begin = 19
        with self.assertRaises(AttributeError):
            period.end = 90
        
    def test_intersection(self):
        """Test the has_intersection method."""
        p1 = Period(0, 10)
        p2 = Period(5, 15)
        p3 = Period(10, 15)

        self.assertTrue(p1.has_intersection(p2))
        self.assertTrue(p2.has_intersection(p1))
        self.assertFalse(p1.has_intersection(p3))
        self.assertFalse(p3.has_intersection(p1))
        self.assertTrue(p2.has_intersection(p3))
        self.assertTrue(p3.has_intersection(p2))

    def test_combine(self):
        """Test the combine feature."""
        p1 = Period(1, 2)
        p2 = Period(2, 3)

        # Check result of combination
        comb = p1 + p2
        self.assertEqual(comb.begin, 1)
        self.assertEqual(comb.end, 3)
        # Check if original objects where not modified
        self.assertEqual(p1.begin, 1)
        self.assertEqual(p2.begin, 2)
        self.assertEqual(p1.end, 2)
        self.assertEqual(p2.end, 3)

        # Check if order matters
        comb = p2 + p1
        self.assertEqual(comb.begin, 1)
        self.assertEqual(comb.end, 3)

        
