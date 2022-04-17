import unittest
from src.Monsters.AbstractMonster import AbstractMonster
from src.Monsters.JawWorm import JawWorm
from src.Actors.ComaActor import ComaAI


class TestJawWorm(unittest.TestCase):

    def test_create(self):
        pass

    def test_take_turn(self):
        pass

    def test_chomp(self):
        """
        Testing that chomp does 11 damage at A < 2
        """
        # Setup
        monster = JawWorm(ascension=1)
        player = ComaAI(cards=[], max_health=100)
        monster.setPlayer(player)

        # Execute
        monster.chomp()

        # Assert
        self.assertEquals(player.current_health, 89)

        """
        Testing that chomp does 12 damage at A >= 2 (Test Edge case 2)
        """
        # Setup
        monster = JawWorm(ascension=2)
        player = ComaAI(cards=[], max_health=100)
        monster.setPlayer(player)

        # Execute
        monster.chomp()

        # Assert
        self.assertEquals(player.current_health, 88)

        """
        Testing that chomp does 12 damage at A >= 2 (Test Edge case 2)
        """
        # Setup
        monster = JawWorm(ascension=2)
        player = ComaAI(cards=[], max_health=100)
        monster.setPlayer(player)

        # Execute
        monster.chomp()

        # Assert
        self.assertEquals(player.current_health, 88)

    def test_thrash(self):
        pass

    def test_bellow(self):
        pass
