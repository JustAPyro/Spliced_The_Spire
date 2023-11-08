from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

from new.effects import Block

if TYPE_CHECKING:
    from actors import AbstractActor
    from enemies import AbstractEnemy


class AbstractCard(ABC):
    """
    Abstract card class is the blueprint for all cards.
    """

    def __init__(self, name: str, energy_cost: int, upgraded: bool = False):
        # Name of the card
        self.name: str = name

        # normal energy cost of card ("cost" int)
        self.energy_cost: int = energy_cost

        # If the card is upgraded or not
        self.upgraded: bool = upgraded

    @abstractmethod
    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy'):
        """Overriding this method provides the default behavior of a card."""
        pass

    @abstractmethod
    def upgrade(self):
        """Overriding this method provides the behavior of the card on upgrade."""
        pass

    # Override the str() method so printing it returns the name
    def __str__(self):
        return self.name

    # Override the repr() method so arrays print neatly
    def __repr__(self):
        return self.name


class RedStrike(AbstractCard, ABC):
    def __init__(self):
        self.damage = 66
        super().__init__(name='Strike', energy_cost=1)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy'):
        caller.deal_damage(target, self.damage)

    def upgrade(self):
        self.damage = 9


class RedDefend(AbstractCard, ABC):
    def __init__(self):
        self.block = 5
        super().__init__(name='Defend', energy_cost=1)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy'):
        caller.apply_block(self.block)

    def upgrade(self):
        self.block = 8


class Bash(AbstractCard, ABC):
    def __init__(self):
        self.damage = 8
        self.vulnerable = 2
        super().__init__(name='Bash', energy_cost=2)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy'):
        target.take_damage(self.damage)
        target.apply_vulnerable(self.vulnerable)

    def upgrade(self):
        self.damage = 10
        self.vulnerable = 3


class Anger(AbstractCard, ABC):
    def __init__(self):
        self.damage = 6
        super().__init__(name='Anger', energy_cost=0)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy'):
        target.take_damage(2)
        caller.discard_pile.append(Anger())

    def upgrade(self):
        self.damage = 8


class BodySlam(AbstractCard, ABC):
    def __init__(self):
        super().__init__("Body Slam", energy_cost=1)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy'):
        # TODO: Implement "caller.get_stacks(Block)"
        target.take_damage(caller.effects.get(Block).stacks)

    def upgrade(self):
        self.energy_cost = 0
