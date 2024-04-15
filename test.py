import unittest
from spliced_the_spire.tests import test_cards, test_e2e_combat

suite = unittest.TestLoader().loadTestsFromModule(test_e2e_combat)
unittest.TextTestRunner(verbosity=2).run(suite)

