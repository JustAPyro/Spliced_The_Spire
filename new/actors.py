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

        self.draw_pile: list[AbstractCard] = clas.start_cards
        self.hand_pile: list[AbstractCard] = []
        self.discard_pile: list[AbstractCard] = []
        self.exhaust_pile: list[AbstractCard] = []

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

    def draw(self, number):
        for i in range(number):
            self.__draw_card()

    def __draw_card(self):
        if len(self.draw_pile) > 0:
            self.hand_pile.append(self.draw_pile.pop())
        elif len(self.discard_pile) > 0:
            self.draw_pile.extend(self.discard_pile)
            self.discard_pile.clear()
            random.shuffle(self.draw_pile)
            self.hand_pile.append(self.draw_pile.pop())


class StupidActor(AbstractActor):
    pass

class PlayerActor(AbstractActor):
    pass
