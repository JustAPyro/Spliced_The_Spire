import unittest
from src.Monsters.TestMonster import TestMonster
from src.Cards.RedStrike import RedStrike


class TestRedStrike(unittest.TestCase):

    def test_use_card(self):
        """
        Test that strike removes 6 health from the enemy
        """
        # Set up
        monster = TestMonster(10)  # Create a test monster to hit with 100 health
        strike = RedStrike()  # Create a strike to use

        # Execute
        strike.useCard(monster)

        # Assert
        self.assertEqual(monster.current_health, 4, "Monster Health Incorrect")
