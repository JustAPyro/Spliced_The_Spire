import unittest
from spliced_the_spire.tests import test_cards

suite = unittest.TestLoader().loadTestsFromModule(test_cards)
unittest.TextTestRunner(verbosity=2).run(suite)

