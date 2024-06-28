import unittest
from spliced_the_spire.tests import test_cards, test_e2e_combat, test_enemies

suite = unittest.TestLoader().loadTestsFromModule(test_enemies)
unittest.TextTestRunner(verbosity=2).run(suite)

