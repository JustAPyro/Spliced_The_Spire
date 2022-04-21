import unittest
from test_utilities import generateSamples
import test_config
from src.Actors.ComaActor import ComaAI
from src.Monsters import Cultist


class TestCultist(unittest.TestCase):
    """
    Test Cultist
    """

    def test_create(self):
        """
        Test Cultist Creation
        :return: None
        """

        """ - - - - - Test that on A5 health is between 48, 54 - - - - - """

        # Set up
        quantity = test_config.test_quantity
        variance = test_config.test_acceptable_variance

        # Execute - Generate 1000 health samples for cultists A5
        health = generateSamples(lambda: Cultist(5).max_health, quantity)

        # Assert
        all(self.assertLessEqual(h, 54) for h in health)     # All health <= 54
        all(self.assertGreaterEqual(h, 46) for h in health)  # All health >= 48
        all(self.assertLess(abs(health[h] - quantity / len(health)), variance) for h in health)

        """ - - - - - Test that on A7 health is between 50, 56 - - - - - """
        # Testing this because it's an edge case

        # Set up
        quantity = test_config.test_quantity
        variance = test_config.test_acceptable_variance

        # Execute - Generate 1000 health samples for cultists A5
        health = generateSamples(lambda: Cultist(7).max_health, quantity)

        # Assert
        all(self.assertLessEqual(h, 56) for h in health)     # All health <= 54
        all(self.assertGreaterEqual(h, 50) for h in health)  # All health >= 48
        all(self.assertLess(abs(health[h] - quantity / len(health)), variance) for h in health)

        """ - - - - - Test that on A7+ (10) health is between 50, 56 - - - - - """
        # Testing this as a base case

        # Set up
        quantity = test_config.test_quantity
        variance = test_config.test_acceptable_variance

        # Execute - Generate 1000 health samples for cultists A5
        health = generateSamples(lambda: Cultist(7).max_health, quantity)

        # Assert
        all(self.assertGreaterEqual(h, 50) for h in health)  # All health >= 48
        all(self.assertLessEqual(h, 56) for h in health)  # All health <= 54
        all(self.assertLess(abs(health[h] - quantity / len(health)), variance) for h in health)

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
        self.assertEqual(4, cultist.getEffect("Ritual"))

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
