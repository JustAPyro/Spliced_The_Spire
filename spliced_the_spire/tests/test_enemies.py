import unittest
from spliced_the_spire.main.abstractions import Room
from spliced_the_spire.main.actors import DummyActor
from spliced_the_spire.main.cards import *
from spliced_the_spire.main.classes import Ironclad
from spliced_the_spire.main.enemies import DummyEnemy


class TestEnemies(unittest.TestCase):

    def test_Louse(self):
        card = Pummel()
        actor = DummyActor(Ironclad, [], health=10, energy=3, hand=[card])
        louse = GreenLouse(
            max_health=13,
            curl_up_stacks=3
        )

        actor.use_card(louse, card)
        

