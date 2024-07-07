from __future__ import annotations

from abc import ABC

from spliced_the_spire.main.abstractions import AbstractActor, AbstractCard
from spliced_the_spire.main.enumerations import SelectEvent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class DummyActor(AbstractActor, ABC):
    def __init__(self, clas, cards, hand, energy, *args, **kwargs):
        super().__init__(clas, cards=cards, hand=hand, *args, **kwargs)

        self.energy = energy
        self.max_energy = energy

        self.logging = False

    def select_card(self, options: list[AbstractCard], event_type: SelectEvent) -> AbstractCard:
        return options[-1]


class LeftToRightAI(AbstractActor):
    def __init__(self, clas, environment, cards):
        super().__init__(clas, environment, cards=cards)

    def turn_logic(self):

        # Pic
        choices = self.get_playable_cards()
        while len(choices) > 0:
            # Find a valid enemy with health remaining
            valid_enemy = None
            for enemy in self.environment['enemies']:
                if enemy.health > 0:
                    valid_enemy = enemy
                    break

            # ??? If no valid, end turn
            if not valid_enemy:
                break

            self.use_card(valid_enemy, choices[0], self.environment['enemies'])
            choices = self.get_playable_cards()

    def select_card(self, options: list[AbstractCard], event_type: SelectEvent) -> AbstractCard:
        if event_type is SelectEvent.COPY:
            return options[-1]
        return options[0]
