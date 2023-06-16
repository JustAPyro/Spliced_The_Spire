from abc import ABC, abstractmethod
from effects import EffectMixin, CURLUP, VULNERABLE
from random import randint
from functools import partial
from typing import TYPE_CHECKING, Dict, Tuple, Optional

from abstraction_enforcement import protect
from AscensionMapping import AscensionBasedInt
from new.ability_patterns import AbilityGenerator

if TYPE_CHECKING:
    from intents import Intent
    from actors import AbstractActor


class AbstractEnemy(ABC, EffectMixin):
    def __init__(self, name, max_health, ascension=0, act=1):
        self.name = name

        # Here we assign max health. We use the provided value but
        # if a dict is provided we calculate a random appropriate max health
        # based on ascension.
        self.max_health = (self.max_health if type(max_health) is not dict
                           else AscensionBasedInt(ascension, max_health))
        # Since this was just created current health should be full
        self.health = self.max_health

        self.intent = None

        # Information about the environment that is relevant to the battle
        self.ascension = ascension
        self.act = act

        super().__init__()

    def is_dead(self):
        return self.health <= 0

    def _trigger_before_damage(self, damage: int):
        curl = False
        for effect in self.effects:
            if effect == CURLUP:
                curl = True

        if curl:
            self.apply_block(self.effects[CURLUP])
            self.negate_effect(CURLUP)

    def take_damage(self, damage: int):
        self._trigger_before_damage(damage)
        if self.has_effect(VULNERABLE):
            damage = damage * 1.5
        self.health -= damage

    def deal_damage(self, damage: int):
        pass

    def set_start(self, health, effects=None, intent=None):
        # TODO: Assert beginning
        self.max_health = health
        self.health = health
        self.clear_effects()

        if effects not None:
            self.apply_all_effects(effects)

        if intent not None:
            self.intent = intent
        return self

    def before_ability(self):
        pass

    def after_ability(self):
        for effect in self.effects:
            if effect == VULNERABLE:
                self.decrease_effect(VULNERABLE, 1)

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


class Cultist(AbstractEnemy):
    max_health_range = {
        0: (48, 54),  # A1- Health is 48-54
        7: (50, 56)  # A7+ Health is 50-56
    }

    def __init__(self, ascension=0):
        super().__init__(name='Cultist',
                         max_health=Cultist.max_health_range,
                         ascension=ascension,
                         act=1)




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
        self.set_effect(CURLUP, AscensionBasedInt(ascension, RedLouse.curl_up_power))

        # TODO: Confirm this? "Between 5  and 7" Inclusive or exclusive?
        self.damage = randint(5, 7)

    @AbstractEnemy.ability
    def bite(self, target=None, damage: Optional[int] = None):
        target.take_damage(damage if damage is not None else
                           self.damage + AscensionBasedInt(self.ascension, RedLouse.bite_value))

    @AbstractEnemy.ability
    def grow(self, quantity: Optional[int] = None):
        self.apply_strength(quantity if quantity is not None else
                            AscensionBasedInt(self.ascension, RedLouse.grow_value))

    @AbstractEnemy.ability_pattern
    def pattern(self):
        ag = AbilityGenerator()
        ag.condition(PercentChance(25, self.grow))

        NotInARow(3, (self.grow, self.bite))
        Percent(25, self.grow),
        Percent(75, self.bite)

        if self.ascension > 17:
            NotInARow(2, self.grow)
