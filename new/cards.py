import random
from abc import ABC, abstractmethod

from typing import TYPE_CHECKING
from enum import Enum
from new.effects import Block, Weak

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
    Abstract card class is the blueprint for all cards. The goal for this class
    is to allow simple, quick implementation of Slay the Spire cards. To use write an implementation
    for a card, write a class that inherits this class as well as ABC, then implement an __init__,
    use, and upgrade_logic methods.
    """

    def __init__(self, energy_cost: int, card_type: CardType, upgraded: bool = False, name: str = None):

        # Name of the card
        if name is None:
            self.name: str = type(self).__name__
        else:
            self.name = name

        # normal energy cost of card ("cost" int)
        self.energy_cost: int = energy_cost

        # If the card is upgraded or not
        self.upgraded: bool = upgraded

        # Type of card
        self.card_type: CardType = card_type

    @abstractmethod
    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', all_enemies):
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

    def is_playable(self, caller):
        """
        Overriding this method allows you to declare when a card is or is not playable.
        The default implementation of this will always return true.
        """
        return True

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

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        caller.deal_damage(target, self.damage)

    def upgrade_logic(self):
        self.damage = 9


class RedDefend(AbstractCard, ABC):
    def __init__(self):
        self.block = 5
        super().__init__(name='Defend', energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        caller.increase_effect(Block, self.block)

    def upgrade_logic(self):
        self.block = 8


class Bash(AbstractCard, ABC):
    def __init__(self):
        self.damage = 8
        self.vulnerable = 2
        super().__init__(energy_cost=2, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        target.take_damage(self.damage)
        target.apply_vulnerable(self.vulnerable)

    def upgrade_logic(self):
        self.damage = 10
        self.vulnerable = 3


class Anger(AbstractCard, ABC):
    def __init__(self):
        self.damage = 6
        super().__init__(energy_cost=0, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        target.take_damage(self.damage)
        caller.discard_pile.append(Anger())

    def upgrade_logic(self):
        self.damage = 8


class Armaments(AbstractCard, ABC):
    def __init__(self):
        self.block = 5
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller, target, enemies):
        caller.apply_block(self.block)
        if self.upgraded:
            for card in caller.hand_pile:
                card.upgrade()
            return
        random.choice(caller.get_hand()).upgrade()

    def upgrade_logic(self):
        self.upgraded = True


class BodySlam(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        # TODO: Implement "caller.get_stacks(Block)"
        if caller.effects.get(Block):
            target.take_damage(caller.effects.get(Block).stacks)

    def upgrade_logic(self):
        self.energy_cost = 0


class Clash(AbstractCard, ABC):

    def __init__(self):
        self.damage = 14
        super().__init__(energy_cost=0, card_type=CardType.ATTACK)

    def use(self, caller, target, enemies):
        target.take_damage(self.damage)

    def upgrade_logic(self):
        self.damage = 18

    def is_playable(self, caller):
        for card in caller.get_hand():
            if card.card_type != CardType.ATTACK:
                return False
        return True


class Cleave(AbstractCard, ABC):
    def __init__(self):
        self.damage = 8
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller, target, enemies):
        for enemy in enemies:
            enemy.take_damage(self.damage)

    def upgrade_logic(self):
        self.damage = 11


class Clothesline(AbstractCard, ABC):
    def __init__(self):
        self.damage = 12
        self.qty_weak = 2
        super().__init__(energy_cost=2, card_type=CardType.ATTACK)

    def use(self, caller, target, enemies):
        target.take_damage(self.damage)
        target.increase_effect(Weak, self.qty_weak)

    def upgrade_logic(self):
        self.damage = 14
        self.qty_weak = 3
