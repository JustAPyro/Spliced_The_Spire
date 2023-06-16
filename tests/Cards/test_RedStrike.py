import unittest
from src.Monsters.TestMonster import TestMonster
from src.Cards.Red import RedStrike


class TestRedStrike(unittest.TestCase):

    def test_use_card(self):

        """
        Test that red strike does 6 damage
        """
        # Set up
        monster = TestMonster(10)  # Create a test monster to hit with 10 health
        strike = RedStrike()

        # Execute
        strike.useCard(monster)

        # Assert
        self.assertEqual(monster.current_health, 4, "Monster Health Incorrect")

    def test_upgrade_card(self):
        """
        Test that card can be upgraded and does 9 damage
        """

        # Set up
        monster = TestMonster(10)
        strike = RedStrike()
        strike.upgrade()

        # Execute
        strike.useCard(monster)

        # Assert
        self.assertEqual(strike.name, "Strike+", 'Name not correctly upgraded.')
        self.assertEqual(monster.current_health, 1, 'Monster Health Incorrect')
