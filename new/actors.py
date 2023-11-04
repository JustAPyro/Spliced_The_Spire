import random

from new.enemies import AbstractEnemy
from new.cards import AbstractCard
from new.effects import EffectMixin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from enemies import AbstractEnemy


class AbstractActor(EffectMixin):
    def __init__(self, clas):
        super().__init__()
        self.name = "Actor"
        self.max_health: int = clas.health
        self.health: int = clas.health
        self.gold: int = 99
        # self.relics = [clas.relic]
        self.max_energy: int = 3
        self.energy: int = 3

        self.draw_pile: list[AbstractCard] = random.sample(clas.start_cards, len(clas.start_cards))
        self.discard_pile: list[AbstractCard] = []
        self.hand = []
        for _ in range(5):
            self.hand.append(self.draw_pile.pop())

    def set_start(self, health, hand):
        # TODO: Assert start
        self.max_health = health
        self.health = health
        self.hand = hand
        return self

    def use_card(self, target: AbstractEnemy, card: AbstractCard):
        if card in self.hand:
            self.hand.remove(card)
        self.energy -= card.energyCost
        card.use(self, target)

    def take_damage(self, damage):
        self.health -= damage

    def end_turn(self):
        pass

    def start_turn(self, draw=None):
        self.energy = self.max_energy
        self.hand = draw if draw else []

class StupidActor(AbstractActor):
    pass

class PlayerActor(AbstractActor):
    pass
