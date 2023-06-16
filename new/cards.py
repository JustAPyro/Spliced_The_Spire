from abc import ABC, abstractmethod

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from actors import AbstractActor
    from enemies import AbstractEnemy


class AbstractCard(ABC):
    """
    Abstract card class is the blueprint for all cards
    """

    def __init__(self, name: str, energy_cost: int):
        # Name of the card
        self.name = name

        # normal energy cost of card ("cost" int)
        self.energyCost = energy_cost

    @abstractmethod
    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy'): pass

    # Override the str() method so printing it returns the name
    def __str__(self):
        return self.name

    # Override the repr() method so arrays print neatly
    def __repr__(self):
        return self.name


class RedStrike(AbstractCard, ABC):
    def __init__(self):
        self.damage = 6
        super().__init__(name='Strike', energy_cost=1)

    def use(self, caller, target):
        target.take_damage(self.damage)


class RedDefend(AbstractCard, ABC):
    def __init__(self):
        self.block = 5
        super().__init__(name='Defend', energy_cost=1)

    def use(self, caller, target):
        caller.apply_block(self.block)


class Bash(AbstractCard, ABC):
    def __init__(self):
        self.damage = 8
        self.apply_vulnerable = 2
        super().__init__(name='Bash', energy_cost=2)

    def use(self, caller, target):
        target.take_damage(8)
        target.apply_vulnerable(self.apply_vulnerable)

