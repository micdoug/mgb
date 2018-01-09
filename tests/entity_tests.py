"""
Unit tests of Entity class.

Authors:
    Michael D. Silva <micdoug.silva@gmail.com>
Created: Jan 2018
Modified: Jan 2018
"""

from unittest import TestCase
from entity import Entity


class EntityTests(TestCase):
    """Unit tests of Entity class."""

    def test_attributes(self) -> None:
        """Test correct and read-only id."""
        # Initialize uid property
        entity = Entity(10)
        self.assertEqual(entity.uid, 10)

        # The id property must be readonly
        with self.assertRaises(AttributeError):
            entity.uid = 15

        # The close_counter must be 0 at first and is readonly
        self.assertEqual(entity.close_counter, 0)
        with self.assertRaises(AttributeError):
            entity.close_counter = 10

        # The away_counter must be 0 at first and is readonly
        self.assertEqual(entity.away_counter, 0)
        with self.assertRaises(AttributeError):
            entity.away_counter = 10

    def test_counters(self) -> None:
        """Test internal counters management."""
        entity = Entity(2)

        self.assertEqual(entity.close_counter, 0)
        self.assertEqual(entity.away_counter, 0)

        entity.increment_away()
        self.assertEqual(entity.close_counter, 0)
        self.assertEqual(entity.away_counter, 1)

        entity.increment_away()
        self.assertEqual(entity.close_counter, 0)
        self.assertEqual(entity.away_counter, 2)

        entity.increment_close()
        self.assertEqual(entity.close_counter, 1)
        self.assertEqual(entity.away_counter, 0)

        entity.increment_close()
        self.assertEqual(entity.close_counter, 2)
        self.assertEqual(entity.away_counter, 0)

    def test_equality(self) -> None:
        """Test entity equality."""
        entity = Entity(3)

        self.assertEqual(entity, 3)
        self.assertEqual(entity, Entity(3))
        self.assertNotEqual(entity, 1)
        self.assertNotEqual(entity, Entity(1))

    def test_is_friend(self):
        """Test is_friend property."""
        Entity.FRIEND_THRESHOLD = 5
        entity = Entity(1)

        self.assertFalse(entity.is_friend)
        entity.increment_close()
        self.assertFalse(entity.is_friend)
        entity.increment_close()
        self.assertFalse(entity.is_friend)
        entity.increment_close()
        self.assertFalse(entity.is_friend)
        entity.increment_close()
        self.assertFalse(entity.is_friend)
        entity.increment_close()
        self.assertTrue(entity.is_friend)
        entity.increment_away()
        self.assertFalse(entity.is_friend)

    def test_is_active(self):
        """Test is_active property."""
        Entity.INACTIVE_THRESHOLD = 2
        entity = Entity(1)

        self.assertTrue(entity.is_active)
        entity.increment_away()
        self.assertTrue(entity.is_active)
        entity.increment_away()
        self.assertFalse(entity.is_active)
        entity.increment_close()
        self.assertTrue(entity.is_active)
