import unittest
from src.Effects import Strength
from src.Monsters import TestMonster
from src.Actors.ComaActor import ComaAI


class TestStrength(unittest.TestCase):

    def test_modifyDamageDealt(self):
        """
        Test that strength increases damage
        """
        # Setup
        monster = TestMonster(100)
        monster.gainStrength(strength=5)
        player = ComaAI(cards=[], max_health=100)
        monster.setPlayer(player)

        # Execute
        monster.deal_damage(10)

        # Assert
        self.assertEqual(85, player.current_health)

