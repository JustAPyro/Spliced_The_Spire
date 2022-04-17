import unittest
from src.Monsters.TestMonsterModule import TestMonster
from src.Cards.RedDefend import RedDefend


class TestRedDefend(unittest.TestCase):

    def test_use_card(self):

        """
        Test that block adds 5 block to the target
        """
        # Set up
        monster = TestMonster(10)  # Create a test monster to hit with 10 health
        defend = RedDefend()  # Create a strike to use

        # Execute
        defend.useCard(monster)

        # Assert
        self.assertEqual(monster.block, 5, "Monster Health Incorrect")
