from abc import ABC, abstractmethod

from new.effects import EffectMixin, Ritual
from random import randint
from typing import TYPE_CHECKING, Optional

from lutil import ascension_based_int
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
    def __init__(self, name, max_health, environment, ascension=0, act=1):
        self.name = name
        # Here we assign max health. We use the provided value but
        # if a dict is provided we calculate a random appropriate max health
        # based on ascension.
        self.max_health = (max_health if type(max_health) is not dict
                           else ascension_based_int(ascension, max_health))
        # Since this was just created current health should be full
        self.health = self.max_health

        # This stores the move pattern of the enemy,
        # It will populate with a generator the first time
        # that take_turn is called on this enemy
        self.ability = self.pattern()

        # Information about the environment that is relevant to the battle
        self.ascension = ascension
        self.act = act

        # Add self to the environment
        if environment:
            self.environment = environment
            self.environment['enemies'].append(self)

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

    def before_ability(self):
        pass

    def after_ability(self):
        pass

    @property
    def intent(self):
        return None

    @staticmethod
    def ability(func):
        def wrapper(*args, **kwargs):
            self = args[0]
            self.before_ability()
            func(*args, **kwargs)
            self.after_ability()

        return wrapper

    @staticmethod
    def ability_pattern(func):
        def wrapper(*args, **kwargs):
            self = args[0]
            func(*args, **kwargs)

        return wrapper

    @abstractmethod
    def pattern(self):
        raise NotImplementedError

    def take_turn(self, actor):
        log = []
        self.process_effects('on_start_turn', self.environment)
        next(self.ability)(actor, None, log)
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
    max_health_range = {
        0: (48, 54),  # A1- Health is 48-54
        7: (50, 56)  # A7+ Health is 50-56
    }
    ritual_gain = {
        +0: 3,  # A0-A1 gain 3 ritual
        +2: 4,  # A2-A16 gain 4 ritual
        17: 5,  # A17+ gain 5 ritual
    }

    def __init__(self, environment=None, ascension=0):
        super().__init__(name='Cultist',
                         max_health=Cultist.max_health_range,
                         environment=environment,
                         ascension=ascension,
                         act=1)

    @AbstractEnemy.ability
    def incantation(self, target, quantity: Optional[int] = None, log=[]):
        log.append('used incantation')
        self.increase_effect(Ritual, quantity if quantity is not None
        else ascension_based_int(self.ascension, Cultist.ritual_gain))

    @AbstractEnemy.ability
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
        self.set_effect(CURLUP, ascension_based_int(ascension, RedLouse.curl_up_power))

        # TODO: Confirm this? "Between 5  and 7" Inclusive or exclusive?
        self.damage = randint(5, 7)

    @AbstractEnemy.ability
    def bite(self, target=None, damage: Optional[int] = None):
        target.take_damage(damage if damage is not None else
                           self.damage + ascension_based_int(self.ascension, RedLouse.bite_value))

    @AbstractEnemy.ability
    def grow(self, quantity: Optional[int] = None):
        self.apply_strength(quantity if quantity is not None else
                            ascension_based_int(self.ascension, RedLouse.grow_value))

    @AbstractEnemy.ability_pattern
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

    @AbstractEnemy.ability
    def Chomp(self, target):
        # Chomp: Deal 11 damage, or 12 on ascension 2+
        target.take_damage(
            ascension_based_int(self.ascension, {
                0: 11,
                2: 12
            }))

    @AbstractEnemy.ability
    def Thrash(self, target):
        # Thrash: Deal 7 damage, gain 5 block.
        self.apply_block(5)
        target.take_damage(7)

    @AbstractEnemy.ability
    def Bellow(self):
        self.apply_strength(ascension_based_int(self.ascension, {
            +0: 3,
            +2: 4,
            17: 5
        }))
        self.apply_block(ascension_based_int(self.ascension, {
            +0: 6,
            17: 9
        }))

    @AbstractEnemy.ability_pattern
    def pattern(self):
        # Simple pattern: casts incantation, then spams dark stroke.
        yield self.incantation
        while True:
            yield self.dark_strike
