import unittest
from Monsters.TestMonster import TestMonster
from Cards.strike_red import StrikeRed


class TestStrikeRed(unittest.TestCase):

    def test_use_card(self):

        """
        Test that strike removes 6 health from the enemy
        """
        # Set up
        monster = TestMonster(10)  # Create a test monster to hit with 10 health
        strike = StrikeRed()  # Create a strike to use

        # Execute
        strike.useCard(monster)

        # Assert
        self.assertEqual(monster.current_health, 4, "Monster Health Incorrect")

