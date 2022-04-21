import unittest

import test_config
from src.Monsters.AbstractMonster import AbstractMonster
from src.Monsters.JawWorm import JawWorm
from src.Actors.ComaActor import ComaAI
from test_utilities import generateSamples


class TestJawWorm(unittest.TestCase):

    def test_create(self):
        """
        Test Jaw Worm Creation
        :return: None
        """

        """ - - - - - Test that on A1 Health is between 40 and 44 - - - - - """

        # Set up
        quantity = test_config.test_quantity
        variance = test_config.test_acceptable_variance

        # Execute - Generate quantity health samples
        health = generateSamples(lambda: JawWorm(1).max_health, quantity)

        # Assert
        all(self.assertGreaterEqual(h, 40) for h in health)  # All health greater/equal to min
        all(self.assertLessEqual(h, 44) for h in health)  # All health less/equal to max
        all(self.assertLess(abs(health[h] - quantity / len(health)), variance) for h in health)

        """ - - - - - Test that on A6 Health is between 40 and 44 - - - - - """
        # Testing because it's an edge case

        # Set up
        quantity = test_config.test_quantity
        variance = test_config.test_acceptable_variance

        # Execute - Generate quantity health samples for
        health = generateSamples(lambda: JawWorm(6).max_health, quantity)

        # Assert
        all(self.assertGreaterEqual(h, 40) for h in health)  # All health greater/equal to min
        all(self.assertLessEqual(h, 44) for h in health)  # All health less/equal to max
        all(self.assertLess(abs(health[h] - quantity / len(health)), variance) for h in health)

        """ - - - - - Test that on A7 Health is between 42 and 46 - - - - - """
        # Testing because it's an edge case

        # Set up
        quantity = test_config.test_quantity
        variance = test_config.test_acceptable_variance

        # Execute - Generate quantity health samples for
        health = generateSamples(lambda: JawWorm(7).max_health, quantity)

        # Assert
        all(self.assertGreaterEqual(h, 42) for h in health)  # All health greater/equal to min
        all(self.assertLessEqual(h, 46) for h in health)  # All health less/equal to max
        all(self.assertLess(abs(health[h] - quantity / len(health)), variance) for h in health)

        """ - - - - - Test that on A10 Health is between 42 and 46 - - - - - """

        # Set up
        quantity = test_config.test_quantity
        variance = test_config.test_acceptable_variance

        # Execute - Generate quantity health samples
        health = generateSamples(lambda: JawWorm(10).max_health, quantity)

        # Assert
        all(self.assertGreaterEqual(h, 42) for h in health)  # All health greater/equal to min
        all(self.assertLessEqual(h, 46) for h in health)  # All health less/equal to max
        all(self.assertLess(abs(health[h] - quantity / len(health)), variance) for h in health)

        """ - - - - - Test that on Act 3 they start with buffs - - - - - """
        # Testing because it's unique behavior

        # Set up
        # None

        # Execute - create a jaw worm on act 3
        j = JawWorm(1, act=3)

        # Assert (on act 3, should have more than 1 strength/block)
        self.assertGreater(1, j.getEffect("Block"))
        self.assertGreater(1, j.getEffect("Strength"))

        """ - - - - - Test that on act 1 they start with Chomp - - - - - """

        # Set up
        actions = []

        # Execute - Generate 1000 health samples for cultists A5
        for i in range(test_config.test_pattern_duration):
            actions.append(JawWorm().take_turn())

        # Assert that it chomped first every time
        all(self.assertEqual(JawWorm._chomp, action) for action in actions)

        """ - - - - - Test that on act 3 they may not start with chomp - - - - - """

        # Set up
        uniqueActions = set()

        # Execute - Generate 1000 health samples for cultists A5
        for i in range(test_config.test_pattern_duration+10):
            uniqueActions.add(JawWorm(act=3).take_turn())

        # Assert that it used 3 unique abilities on its different "first turns"
        self.assertEquals(3, len(uniqueActions))

    def test_take_turn(self):
        """
        TODO: Implement Tests
        Test Jaw Worm Turn Logic
        :return: None
        """
        pass

    def test_chomp(self):
        """
        TODO: Verify Tests
        Test Jaw Worm Chomp Ability
        :return: None
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
        """
        TODO: Implement Tests
        Test Jaw Worm Thrash Ability
        :return: None
        """
        pass

    def test_bellow(self):
        """
        TODO: Implement Tests
        Test Jaw Worm Bellow Ability
        :return: None
        """
        pass
