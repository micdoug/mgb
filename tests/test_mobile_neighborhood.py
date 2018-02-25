"""
Unit tests of MobileNeighborhood class.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: Jan 2018
Modified: Jan 2018
"""

from unittest import TestCase
from mgb.entity import Entity
from mgb.mobile_neighborhood import MobileNeighborhood


class MobileNeighborhoodTests(TestCase):
    """MobileNeighborhood unit tests."""

    def test_constructor(self) -> None:
        """Test basic construction."""
        mn = MobileNeighborhood()

        # Check if is initialized with no members
        self.assertEqual(len(mn.entities.items()), 0)
        self.assertEqual(len(mn), 0)

    def test_add_remove(self) -> None:
        """Test add and remove operations."""
        mn = MobileNeighborhood()

        # Test add
        self.assertFalse(1 in mn)
        self.assertFalse(Entity(1) in mn)
        mn.add(1, 1)
        self.assertTrue(1 in mn)
        self.assertTrue(Entity(1) in mn)

        # Add the same entity should not modify internal object
        old = mn[1]
        mn.add(1, 2)
        self.assertIs(old, mn[1])

        # Test remove
        mn.remove(1)
        self.assertFalse(1 in mn)
        self.assertFalse(Entity(1) in mn)
        mn.remove(1)  # Should fail silently
        self.assertFalse(1 in mn)
        self.assertFalse(Entity(1) in mn)
        
        # Test lenght
        mn.add(1, 2)
        mn.add(2, 2)
        self.assertEqual(len(mn), 2)
        self.assertTrue(1 in mn and 2 in mn)

    def test_intersection(self) -> None:
        """Test intersection method."""
        mn1 = MobileNeighborhood()
        mn2 = MobileNeighborhood()

        mn1.add(1, 1)
        mn1.add(2, 1)
        mn1.add(3, 1)

        mn2.add(1, 1)
        mn2.add(4, 1)
        mn2.add(5, 1)

        intersec = mn1 & mn2
        self.assertSetEqual(intersec, {1})

        mn2.add(2, 1)
        intersec = mn1 & mn2
        self.assertSetEqual(intersec, {1, 2})

        mn1.remove(1)
        mn1.remove(2)
        intersec = mn1 & mn2
        self.assertSetEqual(intersec, set())

    def test_union(self) -> None:
        """Test union method."""
        mn1 = MobileNeighborhood()
        mn2 = MobileNeighborhood()

        mn1.add(1, 1)
        mn1.add(2, 1)
        mn1.add(3, 1)

        mn2.add(1, 1)
        mn2.add(4, 1)
        mn2.add(5, 1)

        intersec = mn1 | mn2
        self.assertSetEqual(intersec, {1, 2, 3, 4, 5})

        mn2.add(2, 1)
        intersec = mn1 | mn2
        self.assertSetEqual(intersec, {1, 2, 3, 4, 5})

        mn1.remove(1)
        mn1.remove(2)
        mn2.remove(2)
        mn2.remove(1)
        intersec = mn1 | mn2
        self.assertSetEqual(intersec, {3, 4, 5})

    def test_is_inactive(self) -> None:
        """Test is_inactive property."""
        Entity.INACTIVE_THRESHOLD = 2
        mn = MobileNeighborhood()
        self.assertTrue(mn.is_active)
        mn.add(1, 1)
        mn.add(2, 2)
        mn.add(3, 3)
        self.assertEqual(mn.started, 1)
        self.assertEqual(mn.ended, 3)
        self.assertTrue(mn.is_active)
        mn[1].increment_away()
        mn[1].increment_away()
        self.assertTrue(mn.is_active)
        mn[2].increment_away()
        mn[2].increment_away()
        self.assertFalse(mn.is_active)
        mn[2].increment_close()
        self.assertTrue(mn.is_active)
        mn[2].increment_away()
        mn[2].increment_away()
        self.assertFalse(mn.is_active)
        mn.add(4, 4)
        self.assertFalse(mn.is_active)

    def test_group_correlation(self) -> None:
        """Test group_correlation method."""
        mn1 = MobileNeighborhood()
        mn2 = MobileNeighborhood()

        self.assertEqual(mn1.group_correlation(mn2), 0)
        mn1.add(1, 1)
        self.assertEqual(mn1.group_correlation(mn2), 0)
        mn2.add(1, 2)
        self.assertEqual(mn1.group_correlation(mn2), 1)
        mn2.add(2, 2)
        self.assertEqual(mn1.group_correlation(mn2), 0.5)
        mn2.add(3, 3)
        mn2.add(4, 3)
        mn2.add(5, 3)
        mn1.add(2, 3)
        self.assertEqual(mn1.group_correlation(mn2), 0.4)
        self.assertEqual(mn1.started, 1)
        self.assertEqual(mn1.ended, 3)
        self.assertEqual(mn2.started, 2)
        self.assertEqual(mn2.ended, 3)
