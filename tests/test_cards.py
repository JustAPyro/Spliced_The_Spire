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
        card = RedDefend()
        actor = DummyActor(Ironclad, [], health=10, energy=3, hand=[card])
        target = DummyEnemy(health=10)

        # Action
        actor.use_card(target, card, [])
        target.deal_damage(5, actor, log=[])

        # Assertions
        self.assertEqual(2, actor.energy)
        self.assertEqual(10, actor.health)

    def test_bash(self):
        card = Bash()
        actor = DummyActor(Ironclad, [], health=10, energy=3, hand=[card])
        target = DummyEnemy(health=10)

        # Action
        actor.use_card(target, card, [])

        # Assertions
        self.assertEqual(1, actor.energy)
        self.assertEqual(2, target.health)
        self.assertEqual(2, target.get_effect_stacks(Vulnerable))

    def test_anger(self):
        card = Anger()
        actor = DummyActor(Ironclad, [], health=10, energy=3, hand=[card])
        target = DummyEnemy(health=10)

        # Action
        actor.use_card(target, card, [])

        # Assertions
        self.assertEqual(3, actor.energy)
        self.assertEqual(4, target.health)
        self.assertEqual(actor.discard_pile[0].name, "Anger")

    def test_armaments(self):
        card = Armaments()
        actor = DummyActor(Ironclad, [], health=10, energy=3, hand=[card, RedStrike()])
        target = DummyEnemy(health=10)

        # Action
        actor.use_card(target, card, [])

        # Assertions
        self.assertEqual(2, actor.energy)
        self.assertEqual(5, actor.get_effect_stacks(Block))
        self.assertEqual(actor.hand_pile[0].upgraded, True)

    def test_bodyslam(self):
        card = BodySlam()
        card2 = RedDefend()
        actor = DummyActor(Ironclad, [], health=10, energy=3, hand=[card, card2])
        target = DummyEnemy(health=10)

        # Action
        actor.use_card(target, card2, [])
        actor.use_card(target, card, [])

        # Assertions
        self.assertEqual(1, actor.energy)
        self.assertEqual(5, actor.get_effect_stacks(Block))
        self.assertEqual(target.health, 5)
