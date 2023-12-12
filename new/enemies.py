from __future__ import annotations

from abc import ABC, abstractmethod

import lutil
from new.effects import EffectMixin, Ritual
from random import randint
from typing import TYPE_CHECKING, Optional

from lutil import asc_int
from new.enumerations import IntentType

if TYPE_CHECKING:
    pass


class Intent:
    """
    A class that encompasses managing the Intent of enemies
    https://slay-the-spire.fandom.com/wiki/Intent
    """
    # The types of Intent that indicate an attack
    # and require a value for incoming damage
    __damage_types = (
        IntentType.AGGRESSIVE,
        IntentType.AGGRESSIVE_DEBUFF,
        IntentType.AGGRESSIVE_DEFENSE,
        IntentType.AGGRESSIVE_BUFF,
    )

    def __init__(self, intent_type: IntentType, damage: int = None):
        """
        Create an intent.

        Parameters
        ----------
        :param intent_type:
            The type of intent. These generally fall
            under a mix of "Aggressive", "Defensive, "Buff" and "Debuff"

        :param damage:
            The amount of damage being dealt for aggressive intents.
        """
        # Some guards to make sure damage values are only appearing when they should.
        if intent_type in self.__damage_types and not damage:
            raise ValueError("Aggressive Intent must have damage amount.")
        if damage and intent_type not in self.__damage_types:
            raise ValueError("Can't provide damage for intents not in __damage_types.")

        # Save the instance variables
        self.intent_type = intent_type
        self.damage = damage


class AbstractEnemy(ABC, EffectMixin):
    """
    This class is an abstract class designed to streamline the implementation
    of enemies and elites.
    https://slay-the-spire.fandom.com/wiki/Monsters
    """

    def __init__(self,
                 name: Optional[str] = None,
                 max_health: dict[tuple[int], Optional[int]] | int | None = None,
                 set_health: Optional[int] = None,
                 ascension=0,
                 environment=None,
                 act=1):
        """
        Create an enemy.

        Parameters
        ----------
        :param name:
            The name of the enemy.
            Note that if this is not provided, the name of the enemy will be parsed from
            the class name.

        :param max_health:
            The creature's max_health. This can be provided in the following format.
            {(lower, upper): None}

        :param set_health:
            If specified will set the health of the creature to this amount.

        Exceptions
        ----------
        :raises RuntimeError:
            This will be thrown if max_health is not provided and the subclass does not
            implement its own static class "max_health" variable.
        """
        # Use the provided name if there is, otherwise parse it from class name
        self.name = name if name else lutil.parse_class_name(type(self).__name__)

        # Guard against people not providing a max_health anywhere
        if not max_health and not hasattr(self, 'max_health'):
            raise RuntimeError(f'Tried to call subclass AbstractEnemy without providing static max_health variable. '
                               f'Please verify that {type(self).__name__}.max_health is a defined value. '
                               f'You may also choose to provide it in the {type(self).__name__}.__init__ constructor.')

        # Assigns a max health based on the ascension and the class.max_health property
        self.max_health = asc_int(ascension, getattr(self, 'max_health'))

        # Since this was just created current health should be full
        self.health = set_health if set_health else self.max_health

        # Information about the environment that is relevant to the battle
        self.ascension = ascension
        self.act = act

        # Add self to the environment
        if environment:
            self.environment = environment
            self.environment['enemies'].append(self)

        # This stores the move pattern of the enemy,
        # It will populate with a generator the first time
        # that take_turn is called on this enemy
        self.ability_method_generator = self.pattern()

        # Initialize the EffectMixin
        super().__init__()

    def is_dead(self):
        return self.health <= 0

    def take_damage(self, damage: int):
        damage = self.process_effects('modify_damage_taken', self.environment, damage)
        self.health -= damage

    def deal_damage(self, damage: int, target, log):
        damage = self.process_effects('modify_damage_dealt', self.environment, damage)
        log.append(f'used Dark Strike on {target.name} to deal {damage} damage.')
        target.take_damage(damage, self)

    @property
    def intent(self):
        return None

    @abstractmethod
    def pattern(self):
        raise NotImplementedError

    def take_turn(self, actor):
        log = []
        self.process_effects('on_start_turn', self.environment)
        next(self.ability_method_generator)(actor, None, log)
        self.process_effects('on_end_turn', self.environment)
        return log[0]


class DummyEnemy(AbstractEnemy, ABC):
    def __init__(self, environment, health=10, ascension=0):
        super().__init__(name='Dummy',
                         max_health=health,
                         ascension=ascension,
                         act=1,
                         environment=environment)
        self.environment = environment

    def pattern(self):
        pass





class Cultist(AbstractEnemy):
    max_health = {
        0: (48, 54),  # Health is 48-54 on A0+
        7: (50, 56)  # Health is 50-56 on A7+
    }
    # The amount of ritual gained by ascension
    ritual_gain = {
        +0: 3,
        +2: 4,
        17: 5
    }

    def __init__(self, environment=None, ascension=0):
        super().__init__(environment=environment,
                         ascension=ascension,
                         act=1)

    def incantation(self, target, quantity: Optional[int] = None, log=[]):
        log.append('used incantation')
        self.increase_effect(Ritual, quantity if quantity is not None
        else asc_int(self.ascension, Cultist.ritual_gain))

    def dark_strike(self, target, damage: Optional[int] = None, log=[]):
        self.deal_damage(6, target, log)

    def pattern(self):
        # Simple pattern: casts incantation, then spams dark stroke.
        yield self.incantation
        while True:
            yield self.dark_strike


class RedLouse(AbstractEnemy):
    max_health_range = {
        0: (10, 15),
        7: (11, 16)
    }
    new_max_health = {
        (48, 54): None,
        (50, 56): 7
    }
    curl_up_power = {
        +0: (3, 7),
        +7: (4, 8),
        17: (9, 12)
    }
    bite_value = {
        0: 0,  # Deals D + 0 damage on A0
        2: 1,  # Deals D + 1 damage on A2+
    }
    grow_value = {
        +0: 3,
        17: 4,
    }

    def __init__(self, ascension=0):
        super().__init__(name='Louse',
                         max_health=RedLouse.max_health_range,
                         ascension=ascension,
                         act=1)

        # Calculate a random curl up power based on value map
        self.set_effect(CURLUP, asc_int(ascension, RedLouse.curl_up_power))

        # TODO: Confirm this? "Between 5  and 7" Inclusive or exclusive?
        self.damage = randint(5, 7)

    def bite(self, target=None, damage: Optional[int] = None):
        target.take_damage(damage if damage is not None else
                           self.damage + asc_int(self.ascension, RedLouse.bite_value))

    def grow(self, quantity: Optional[int] = None):
        self.apply_strength(quantity if quantity is not None else
                            asc_int(self.ascension, RedLouse.grow_value))

    def pattern(self):
        yield self.bite


class Jaw_Worm(AbstractEnemy):
    max_health_range = {
        0: (40, 44),  # A1- Health is 48-54
        7: (42, 46)  # A7+ Health is 50-56
    }

    def __init__(self, ascension=0, act=1):
        super().__init__(name='Jaw Worm',
                         max_health=Jaw_Worm.max_health_range,
                         ascension=ascension,
                         act=act)

    def Chomp(self, target):
        # Chomp: Deal 11 damage, or 12 on ascension 2+
        target.take_damage(
            asc_int(self.ascension, {
                0: 11,
                2: 12
            }))

    def Thrash(self, target):
        # Thrash: Deal 7 damage, gain 5 block.
        self.apply_block(5)
        target.take_damage(7)

    def Bellow(self):
        self.apply_strength(asc_int(self.ascension, {
            +0: 3,
            +2: 4,
            17: 5
        }))
        self.apply_block(asc_int(self.ascension, {
            +0: 6,
            17: 9
        }))

    def pattern(self):
        # Simple pattern: casts incantation, then spams dark stroke.
        yield self.incantation
        while True:
            yield self.dark_strike
