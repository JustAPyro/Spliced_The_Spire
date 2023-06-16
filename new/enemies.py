from abc import ABC, abstractmethod
from effects import EffectMixin, CURLUP, VULNERABLE
from random import randint
from functools import partial
from typing import TYPE_CHECKING, Dict, Tuple

from AscensionMapping import AscensionBasedInt

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

    def action(self, target, action):
        action.do(self, target)

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

    def set_start(self, health, effects, intent):
        # TODO: Assert beginning
        self.max_health = health
        self.health = health
        self.clear_effects()
        self.apply_all_effects(effects)
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


class RedLouse(AbstractEnemy):
    max_health_range = {
        0: (10, 15),
        7: (11, 16)
    }
    curl_up_power = {
        0: (3, 7),
        7: (4, 8),
        17: (9, 12)
    }
    bite_damage_boost = {
        0: 0,  # Deals D + 0 damage on A0
        2: 1,  # Deals D + 1 damage on A2+
    }

    def __init__(self, ascension=0):
        super().__init__(name="Louse",
                         max_health=RedLouse.max_health_range,
                         ascension=ascension,
                         act=1)

        # Calculate a random curl up power based on value map
        self.set_effect(CURLUP, AscensionBasedInt(ascension, RedLouse.curl_up_power))

        # TODO: Confirm this? "Between 5  and 7" Inclusive or exclusive?
        self.damage = randint(5, 7)
        self.bite_damage = {
            0: ()
        }

    @AbstractEnemy.ability
    def bite(self, target=None, damage=None):
        target.take_damage(damage if damage is not None else
                           self.damage + AscensionBasedInt(
                               self.ascension,
                               RedLouse.bite_damage_boost
                           ))

    @AbstractEnemy.ability
    def grow(self, quantity):
        self.apply_strength(quantity)
