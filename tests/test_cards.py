import unittest

from new.actors import DummyActor
from new.cards import *
from new.classes import Ironclad
from new.enemies import DummyEnemy


class TestCards(unittest.TestCase):

    def test_red_strike(self):
        # Setup
        card = RedStrike()
        actor = DummyActor(Ironclad, [], health=10, energy=3, hand=[card])
        target = DummyEnemy(health=10)

        # Action
        actor.use_card(target, card, [])

        # Assertions
        self.assertEqual(4, target.health)
        self.assertEqual(2, actor.energy)

    def test_red_defend(self):
        pass
