import unittest
from src.Actors.ComaActor import ComaAI
from src.Monsters import Cultist


class TestCultist(unittest.TestCase):
    """
    Test Cultist
    """

    def test_create(self):
        """
        TODO: Implement tests
        Test Cultist Creation
        :return:
        """
        pass

    def test_take_turn(self):
        """
        TODO: Implement tests
        Testing Cultist Turn
        :return:
        """
        pass

    def test_incantation(self):
        """
        Testing Cultist Incantation
        :return: None
        """
        """ - - - - - Test that A1 gives 3 Ritual - - - - - """
        # Setup
        cultist = Cultist(1)

        # Execute
        cultist._incantation()

        # Assert
        self.assertEqual(3, cultist.getEffect("Ritual"))

        """ - - - - - Test that A2 gives 4 Ritual - - - - - """
        # Setup
        cultist = Cultist(2)

        # Execute
        cultist._incantation()

        # Assert
        self.assertEqual(4, cultist.getEffect("Ritual"))

        """ - - - - - Test that A16 gives 4 Ritual - - - - - """
        # Setup
        cultist = Cultist(16)

        # Execute
        cultist._incantation()

        # Assert
        self.assertEqual(5, cultist.getEffect("Ritual"))

        """ - - - - - Test that A17 gives 5 Ritual - - - - - """
        # Setup
        cultist = Cultist(17)

        # Execute
        cultist._incantation()

        # Assert
        self.assertEqual(5, cultist.getEffect("Ritual"))

        """ - - - - - Test that A20 gives 5 Ritual - - - - - """
        # Setup
        cultist = Cultist(20)

        # Execute
        cultist._incantation()

        # Assert
        self.assertEqual(5, cultist.getEffect("Ritual"))

    def test_darkStrike(self):
        """
        Testing Cultist Dark Strike
        :return: None
        """

        """ - - - - - Test that Dark Strike does 6 Damage - - - - - """
        # Setup
        cultist = Cultist()
        player = ComaAI(cards=[], max_health=100)
        cultist.setPlayer(player)

        # Execute
        cultist._darkStrike()

        # Assert
        self.assertEqual(94, player.current_health)
