import unittest
from src.Utility.HomeUtility import RandomChance, DoesNotAddTo100, ChanceNotDeclared


class TestHomeUtility(unittest.TestCase):

    def test_create(self):
        """
        Test that creating a RandomChance with things that don't add up will raise an DoesNotAddTo100 exception
        """
        self.assertRaises(DoesNotAddTo100, RandomChance, 1, 5)

        self.assertRaises(DoesNotAddTo100, RandomChance, 33, 33, 33)

        self.assertRaises(DoesNotAddTo100, RandomChance, 10, -90)

        self.assertRaises(DoesNotAddTo100, RandomChance, 1, 50)

        self.assertRaises(DoesNotAddTo100, RandomChance, 99, 2)

        """
        Test that using an undeclared chance raises and error
        """
        # Set up
        rc = RandomChance(25, 75)

        # Assert Exception
        self.assertRaises(ChanceNotDeclared, rc.chance, 50)




