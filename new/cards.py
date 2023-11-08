import random
from abc import ABC, abstractmethod

from typing import TYPE_CHECKING
from enum import Enum
from new.effects import Block

if TYPE_CHECKING:
    from actors import AbstractActor
    from enemies import AbstractEnemy


class CardType(Enum):
    ATTACK = 1
    SKILL = 2
    POWER = 3
    STATUS = 4
    CURSE = 5


class AbstractCard(ABC):
    """
    Abstract card class is the blueprint for all cards.
    """

    def __init__(self, name: str, energy_cost: int, card_type: CardType, upgraded: bool = False):
        # Name of the card
        self.name: str = name

        # normal energy cost of card ("cost" int)
        self.energy_cost: int = energy_cost

        # If the card is upgraded or not
        self.upgraded: bool = upgraded

        # Type of card
        self.card_type: CardType = card_type

    @abstractmethod
    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy'):
        """Overriding this method provides the default behavior of a card."""
        pass

    def upgrade(self):
        if self.upgraded:
            return

        self.name = self.name + "+"
        self.upgraded = True
        self.upgrade_logic()

    @abstractmethod
    def upgrade_logic(self):
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
        self.damage = 6
        super().__init__(name='Strike', energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy'):
        caller.deal_damage(target, self.damage)

    def upgrade_logic(self):
        self.damage = 9


class RedDefend(AbstractCard, ABC):
    def __init__(self):
        self.block = 5
        super().__init__(name='Defend', energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy'):
        caller.apply_block(self.block)

    def upgrade_logic(self):
        self.block = 8


class Bash(AbstractCard, ABC):
    def __init__(self):
        self.damage = 8
        self.vulnerable = 2
        super().__init__(name='Bash', energy_cost=2, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy'):
        target.take_damage(self.damage)
        target.apply_vulnerable(self.vulnerable)

    def upgrade_logic(self):
        self.damage = 10
        self.vulnerable = 3


class Anger(AbstractCard, ABC):
    def __init__(self):
        self.damage = 6
        super().__init__(name='Anger', energy_cost=0, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy'):
        target.take_damage(self.damage)
        caller.discard_pile.append(Anger())

    def upgrade_logic(self):
        self.damage = 8


class Armaments(AbstractCard, ABC):
    def __init__(self):
        self.block = 5
        super().__init__("Armaments", energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller, target):
        caller.apply_block(self.block)
        if self.upgraded:
            for card in caller.hand_pile:
                card.upgrade()
            return
        random.choice(caller.hand_pile).upgrade()

    def upgrade_logic(self):
        self.upgraded = True


class BodySlam(AbstractCard, ABC):
    def __init__(self):
        super().__init__("Body Slam", energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy'):
        # TODO: Implement "caller.get_stacks(Block)"
        if (caller.effects.get(Block)):
            target.take_damage(caller.effects.get(Block).stacks)

    def upgrade_logic(self):
        self.energy_cost = 0
