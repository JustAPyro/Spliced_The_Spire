import unittest
from spliced_the_spire.main.abstractions import Room
from spliced_the_spire.main.actors import DummyActor
from spliced_the_spire.main.cards import *
from spliced_the_spire.main.classes import Ironclad
from spliced_the_spire.main.enemies import DummyEnemy


class TestCards(unittest.TestCase):

    def test_Wound(self):
        card = Wound()
        actor = DummyActor(Ironclad, [], health=10, energy=3, hand=[card])

        playable = actor.get_playable_cards()

        self.assertNotIn(card, playable)

    def test_red_strike(self):
        # Setup
        card = RedStrike()
        actor = DummyActor(Ironclad, [], health=10, energy=3, hand=[card])
        target = DummyEnemy(health=10)

        # Action
        actor.use_card(target, card)

        # Assertions
        self.assertEqual(4, target.health)
        self.assertEqual(2, actor.energy)

    def test_red_defend(self):
        card = RedDefend()
        actor = DummyActor(Ironclad, [], health=10, energy=3, hand=[card])
        target = DummyEnemy(health=10, target=actor)

        # Action
        actor.use_card(target, card)
        target.deal_damage(5)

        # Assertions
        self.assertEqual(2, actor.energy)
        self.assertEqual(10, actor.health)

    def test_bash(self):
        card = Bash()
        actor = DummyActor(Ironclad, [], health=10, energy=3, hand=[card])
        target = DummyEnemy(health=10)

        # Action
        actor.use_card(target, card)

        # Assertions
        self.assertEqual(1, actor.energy)
        self.assertEqual(2, target.health)
        self.assertEqual(2, target.get_effect_stacks(Vulnerable))

    def test_anger(self):
        card = Anger()
        actor = DummyActor(Ironclad, [], health=10, energy=3, hand=[card])
        target = DummyEnemy(health=10)

        # Action
        actor.use_card(target, card)

        # Assertions
        self.assertEqual(3, actor.energy)
        self.assertEqual(4, target.health)
        self.assertEqual(actor.discard_pile[0].name, "Anger")

    def test_armaments(self):
        card = Armaments()
        actor = DummyActor(Ironclad, [], health=10, energy=3, hand=[card, RedStrike()])
        target = DummyEnemy(health=10)

        # Action
        actor.use_card(target, card)

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
        actor.use_card(target, card2)
        actor.use_card(target, card)

        # Assertions
        self.assertEqual(1, actor.energy)
        self.assertEqual(5, actor.get_effect_stacks(Block))
        self.assertEqual(target.health, 5)

    def test_clash(self):
        # ---- Test for 14 damage and correct energy usage
        card = Clash()
        actor = DummyActor(Ironclad, cards=[], health=10, energy=3, hand=[card])
        target = DummyEnemy(health=20)

        actor.use_card(target, card)

        self.assertEqual(6, target.health)
        self.assertEqual(3, actor.energy)

        # ---- Test to make sure you can't use it with a non-attack in your hand
        card = Clash()
        card2 = RedDefend()
        actor = DummyActor(Ironclad, cards=[], health=10, energy=3, hand=[card, card2])
        target = DummyEnemy(health=20)

        self.assertTrue(card not in actor.get_playable_cards())
        exception = None
        try:
            actor.use_card(target, card)
        except CardNotPlayable as e:
            exception = e
        self.assertIsNotNone(exception)

        # ---- Test upgraded damage
        card = Clash()
        card.upgrade()
        actor = DummyActor(Ironclad, cards=[], health=10, energy=3, hand=[card])
        target = DummyEnemy(health=20)

        actor.use_card(target, card)

        self.assertEqual(2, target.health)
        self.assertEqual(3, actor.energy)

    def test_cleave(self):
        card = Cleave()
        target = DummyEnemy(health=20)
        target2 = DummyEnemy(health=20)
        actor = DummyActor(Ironclad, cards=[], health=10, energy=3, hand=[card])

        # Note, the following are also fine, just not as concise
        # room = Room(actor, [target, target2]) -> room is unused variable
        # room = Room(actor=actor, enemies=[target,target2]) -> Maybe more readable? Also more boilerplate
        # It's a little weird, because just the act of creating the room links everything, but pretty neat
        _ = Room(actor, [target, target2])

        actor.use_card(target, card)

        self.assertEqual(12, target.health)
        self.assertEqual(12, target2.health)

        # You can also create a room first, and then add things into it, if you prefer. Same end result.
        # This style means you don't need variable names for everything, which
        # is nice because you don't have to do target, target2, etc..., But also annoying
        # because you DO need a reference to actor to use the card.
        card = Cleave()
        card.upgrade()

        rm = Room()
        rm.set_actor(DummyActor(Ironclad, cards=[], health=10, energy=3, hand=[card]))
        rm.add_enemy(DummyEnemy(health=20))
        rm.add_enemy(DummyEnemy(health=20))

        rm.actor.use_card(None, card)

        for enemy in rm.enemies:
            self.assertEqual(9, enemy.health)

    def test_clothesline(self):
        card = Clothesline()
        target = DummyEnemy(health=20)
        actor = DummyActor(Ironclad, cards=[], health=10, energy=3, hand=[card])

        _ = Room(actor, [target])

        actor.use_card(target, card)

        self.assertEqual(8, target.health)
        self.assertEqual(2, target.get_effect_stacks(Weak))

    def test_flex(self):
        card = Flex()
        target = DummyEnemy(health=20)
        actor = DummyActor(Ironclad, cards=[], health=10, energy=3, hand=[card])
        _ = Room(actor, [target])
        actor.use_card(target, card)
        self.assertEqual(2, actor.get_effect_stacks(Strength))


if __name__ == '__main__':
    unittest.main()
