import unittest

from actors import AbstractActor
from cards import RedDefend, RedStrike, Bash
from enemies import RedLouse, Cultist
from classes import Ironclad
from intents import Attack, Buff
from effects import CURLUP, VULNERABLE, BLOCK, STRENGTH, RITUAL


class TestRealizedBattle(unittest.TestCase):
    def test_battle_06_16_23_01(self):
        player = AbstractActor(Ironclad).set_start(
            health=88,
            hand=[RedDefend(), RedStrike(), RedDefend(), Bash(), RedStrike()]
        )
        left_louse = RedLouse().set_start(
            health=15,
            effects=[(CURLUP, 4)],
            intent=Attack(7))
        right_louse = RedLouse().set_start(
            health=11,
            effects=[(CURLUP, 4)],
            intent=Buff()
        )
        self.assertEqual(player.health, 88)
        self.assertEqual(player.energy, 3)
        self.assertEqual(player.gold, 99)
        self.assertEqual(left_louse.health, 15)
        self.assertEqual(right_louse.health, 11)
        self.assertEqual(len(player.hand), 5)

        player.use_card(left_louse, player.hand[3])

        self.assertEqual(left_louse.health, 7, 'Louse took correct amount of damage')
        self.assertTrue(left_louse.has_effect(VULNERABLE, 2), 'Bash applied vulnerable correctly')
        self.assertTrue(left_louse.has_effect(BLOCK, 4), 'Curlup correctly converted to block')
        self.assertTrue(left_louse.has_effect(CURLUP, 0), 'Curlup correctly expired')
        self.assertEqual(player.energy, 1, 'Player energy was correctly used')
        self.assertEqual(len(player.hand), 4, 'Player lost a card')

        player.use_card(right_louse, player.hand[1])

        self.assertEqual(right_louse.health, 5, 'Louse took correct amount of damage')
        self.assertTrue(right_louse.has_effect(BLOCK, 4), 'Curlup correctly converted to block')
        self.assertTrue(right_louse.has_effect(CURLUP, 0), 'Curlup correctly expired')
        self.assertEqual(player.energy, 0, 'Player energy was correctly used')
        self.assertEqual(len(player.hand), 3, 'Player lost a card')

        player.end_turn()
        left_louse.bite(player, 7)
        right_louse.grow(3)
        player.start_turn(draw=[RedDefend(), RedStrike(), RedDefend(), RedStrike(), RedStrike])

        self.assertEqual(player.energy, 3, 'player has regenerated energy')
        self.assertEqual(player.health, 81, 'player took appropriate damage')
        self.assertEqual(len(player.hand), 5, 'player redrew hand')
        self.assertTrue(left_louse.has_effect(VULNERABLE, 1), 'Vulnerable went down')
        self.assertTrue(right_louse.has_effect(STRENGTH, 3), 'louse received strength')

        player.use_card(left_louse, player.hand[1])
        player.use_card(right_louse, player.hand[2])

        self.assertEqual(left_louse.health, -2, 'damage while vulnerable applied correctly')
        self.assertTrue(left_louse.is_dead(), 'left louse is dead')
        self.assertEqual(right_louse.health, -1, 'damage applied correctly')
        self.assertTrue(right_louse.is_dead(), 'right louse is dead')
        self.assertEqual(player.energy, 1, 'player is at correct energy')

    def test_battle_06_16_23_02(self):
        player = AbstractActor(Ironclad).set_start(
            health=88,
            hand=[RedStrike(), RedDefend(), Bash(), RedStrike(), RedDefend()]
        )
        cultist = Cultist().set_start(
            health=54,
        )

        self.assertEqual(88, player.health, 'player health check')
        self.assertEqual(3, player.energy, 'player energy check')
        self.assertEqual(54, cultist.health, 'enemy health check')

        player.use_card(cultist, player.hand[2])
        player.use_card(cultist, player.hand[0])
        player.end_turn()

        self.assertEqual(0, player.energy, 'player energy depleted')
        self.assertEqual(37, cultist.health, 'enemy health check')
        self.assertTrue(cultist.has_effect(VULNERABLE, 2))

        cultist.incantation(3)

        self.assertTrue(cultist.has_effect(RITUAL, 3))
        self.assertTrue(cultist.has_effect(VULNERABLE, 1))
        self.assertEqual(37, cultist.health)
        self.assertEqual(88, player.health)
        player.start_turn([RedDefend(), RedStrike(), RedStrike(), RedStrike(), RedDefend()])
        player.use_card(cultist, player.hand[1])
        player.use_card(cultist, player.hand[1])
        player.use_card(cultist, player.hand[1])

        self.assertEqual(len(player.hand), 2)
        self.assertEqual(10, cultist.health)
        self.assertTrue(cultist.has_effect(VULNERABLE, 1))

        player.end_turn()
        cultist.dark_strike(player, 6)
        player.start_turn([RedStrike(), RedDefend(), Bash(), RedDefend(), RedStrike()])

        self.assertFalse(cultist.has_effect(VULNERABLE))
        self.assertEqual(82, player.health)
        self.assertEqual(5, len(player.hand))
        self.assertEqual(3, player.energy)
        self.assertTrue(cultist.has_effect(STRENGTH, 3))
        self.assertTrue(cultist.has_effect(RITUAL, 3))
        player.use_card(cultist, player.hand[2])
        player.use_card(cultist, player.hand[0])

        self.assertEqual(-7, cultist.health)
        self.assertTrue(cultist.has_effect(VULNERABLE, 2))
        self.assertTrue(cultist.is_dead())




