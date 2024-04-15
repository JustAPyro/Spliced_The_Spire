import unittest
from spliced_the_spire.main.cards import RedStrike, RedDefend, Bash
from spliced_the_spire.main.actors import DummyActor
from spliced_the_spire.main.classes import Ironclad
from spliced_the_spire.main.effects import Block, Vulnerable, CurlUp
from spliced_the_spire.main.abstractions import Room, CardPiles
from spliced_the_spire.main.enemies import GreenLouse
class TestEndToEndCombat(unittest.TestCase):
    def test_e2e_combat(self):

        # Combat setup

        draw_pile = [
            RedStrike(),
            RedStrike(),
            RedDefend(),
            RedDefend(),
            RedDefend(),
        ]

        hand_pile = [
            RedStrike(upgraded=True),
            RedStrike(),
            RedStrike(),
            Bash(),
            RedDefend()
        ]



        actor = DummyActor(Ironclad,
                           cards=draw_pile, 
                           hand=hand_pile,
                           health=80,
                           max_health=80, 
                           energy=3)

        left_green_louse = GreenLouse(
            max_health=13,
            curl_up_stacks=3
        )
        right_green_louse = GreenLouse(
            max_health=12,
            curl_up_stacks=6
        )

        room = Room(actor=actor)
        room.add_enemy(left_green_louse)
        room.add_enemy(right_green_louse)


        # NOTE: These assertions don't really matter, and are more for me to be sure
        # that I'm setting up the test case correctly. Feel free to ignore them and just
        # assume that the scene is set up correctly for other tests.
        
        self.assertEquals(80, actor.health)
        self.assertEquals(80, actor.max_health)

        self.assertEquals(13, room.enemies[0].health)
        self.assertEquals(13, room.enemies[0].max_health)
        self.assertEquals(0, room.enemies[0].get_effect_stacks(Block))
        self.assertEquals(3, room.enemies[0].get_effect_stacks(CurlUp))
        self.assertEquals(12, room.enemies[1].health)
        self.assertEquals(12, room.enemies[1].max_health)
        self.assertEquals(0, room.enemies[0].get_effect_stacks(Block))
        self.assertEquals(3, room.enemies[0].get_effect_stacks(CurlUp))
        
        self.assertEquals(3, actor.energy)
        self.assertEquals(3, actor.max_energy)
       
        self.assertCountEqual(hand_pile, actor.get_cards(from_piles=CardPiles.HAND))

        # START COMBAT

        # T1.C1, Bash on Left Green Louse:
        actor.use_card(room.enemies[0], actor.get_card(with_names='Bash'))

        # Assert the correct energy, health, and effects
        self.assertEqual(actor.energy, 1)

        self.assertEqual(5, room.enemies[0].health)
        self.assertEqual(0, room.enemies[0].get_effect_stacks(CurlUp))
        self.assertEqual(2, room.enemies[0].get_effect_stacks(Vulnerable))
        self.assertEqual(3, room.enemies[0].get_effect_stacks(Block))
        self.assertEqual(12, room.enemies[1].health)

        # T1.C2, Strike+ on Left Green Louse:
        actor.use_card(room.enemies[0], actor.get_card(with_names='Strike', upgraded=True))

        self.assertEqual(0, actor.energy)
        self.assertTrue(left_green_louse.is_dead())
        

