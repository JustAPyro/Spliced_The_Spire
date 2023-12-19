import unittest

from spliced_the_spire.new.actors import DummyActor
from spliced_the_spire.new.cards import *
from spliced_the_spire.new.classes import Ironclad
from spliced_the_spire.new.enemies import DummyEnemy


class TestCards(unittest.TestCase):

    def test_Wound(self):
        card = Wound()
        actor = DummyActor(Ironclad, [], health=10, energy=3, hand=[card], environment={})

        playable = actor.get_playable_cards()

        self.assertNotIn(card, playable)

    def test_red_strike(self):
        # Setup
        card = RedStrike()
        actor = DummyActor(Ironclad, [], health=10, energy=3, hand=[card], environment={})
        target = DummyEnemy(health=10, environment={})

        # Action
        actor.use_card(target, card, [])

        # Assertions
        self.assertEqual(4, target.health)
        self.assertEqual(2, actor.energy)

        actor.hand_pile = [card]
        actor.energy = 3
        target.health = 10
        card.upgrade()
        actor.use_card(target, card, [])
        self.assertEqual(1, target.health)
        self.assertEqual(2, actor.energy)

    def test_red_defend(self):
        card = RedDefend()
        actor = DummyActor(Ironclad, [], health=10, energy=3, hand=[card], environment={})
        target = DummyEnemy(health=10, environment={})

        # Action
        actor.use_card(target, card, [])
        target.deal_damage(5, actor, log=[])

        # Assertions
        self.assertEqual(2, actor.energy)
        self.assertEqual(10, actor.health)

        actor.energy = 3
        actor.clear_effects()
        card.upgrade()
        actor.hand_pile = [card]
        actor.use_card(target, card, [])
        target.deal_damage(10, actor, log=[])
        self.assertEqual(2, actor.energy)
        self.assertEqual(8, actor.health)

    def test_bash(self):
        card = Bash()
        actor = DummyActor(Ironclad, [], health=10, energy=3, hand=[card], environment={})
        target = DummyEnemy(health=10, environment={})

        # Action
        actor.use_card(target, card, [])

        # Assertions
        self.assertEqual(1, actor.energy)
        self.assertEqual(2, target.health)
        self.assertEqual(2, target.get_effect_stacks(Vulnerable))

    def test_anger(self):
        card = Anger()
        actor = DummyActor(Ironclad, [], health=10, energy=3, hand=[card], environment={})
        target = DummyEnemy(health=10, environment={})

        # Action
        actor.use_card(target, card, [])

        # Assertions
        self.assertEqual(3, actor.energy)
        self.assertEqual(4, target.health)
        self.assertEqual(actor.discard_pile[0].name, "Anger")

    def test_armaments(self):
        card = Armaments()
        actor = DummyActor(Ironclad, [], health=10, energy=3, hand=[card, RedStrike()], environment={})
        target = DummyEnemy(health=10, environment={})

        # Action
        actor.use_card(target, card, [])

        # Assertions
        self.assertEqual(2, actor.energy)
        self.assertEqual(5, actor.get_effect_stacks(Block))
        self.assertEqual(actor.hand_pile[0].upgraded, True)

    def test_bodyslam(self):
        card = BodySlam()
        card2 = RedDefend()
        actor = DummyActor(Ironclad, [], health=10, energy=3, hand=[card, card2], environment={})
        target = DummyEnemy(health=10, environment={})

        # Action
        actor.use_card(target, card2, [])
        actor.use_card(target, card, [])

        # Assertions
        self.assertEqual(1, actor.energy)
        self.assertEqual(5, actor.get_effect_stacks(Block))
        self.assertEqual(target.health, 5)
