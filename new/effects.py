from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from actors import AbstractActor
    from enemies import AbstractEnemy

BLOCK = 'BLOCK'
CURLUP = 'CURLUP'
VULNERABLE = 'VULNERABLE'
STRENGTH = 'STRENGTH'
RITUAL = 'RITUAL'


class AbstractEffect:
    def __init__(self):
        self.stacks = 0

    def decrease_stacks(self: AbstractEffect, quantity: int = 1) -> int:
        """Decrease the number of stacks of this effect by quantity. Return the number removed."""
        # Refactored 11/5/2023, LH

        # If this resulted in negative set to 0
        # And say we removed the number that existed
        if self.stacks - quantity < 0:
            removed = self.stacks
            self.stacks = 0
            return removed

        # Otherwise we reduce it by quantity
        # and return that
        self.stacks = self.stacks - quantity
        return quantity

    def increase_stacks(self: AbstractEffect, quantity: int = 1):
        self.stacks += quantity

    # API METHODS

    def modify_damage_taken(self, damage: int) -> int:
        pass


class Block(AbstractEffect):
    def modify_damage_taken(self: AbstractEffect, damage: int) -> int:
        # This tries to decrease the number of block by the damage,
        # and returns how many block were actually removed
        stacks_removed = self.decrease_stacks(damage)

        # To modify damage by the number of stacks we return the
        # negative of that
        return -1 * stacks_removed


class Vulnerable(AbstractEffect):
    def modify_damage_taken(self, damage: int) -> int:
        # Vulnerable adds 50% damage
        return int(damage * .5)

class Ritual(AbstractEffect):
    pass

class Strength(AbstractEffect):
    pass

class EffectMixin:
    """
    This EffectMixin class is added to both the actors and the enemies, and allows for
    managing different effects.
    """
    def __init__(self):
        self.damage_prevention = 0
        self.ritual_flag: bool = False
        self.effects: dict[type[AbstractEffect], AbstractEffect] = {}

    def get_effects_dict(self):
        effects_dict = {}
        for effect in self.effects:
            effects_dict[effect.__name__] = self.effects[effect].stacks
        return effects_dict

    def get_effect_stacks(self: AbstractActor, effect_str: str) -> int:
        """Return the number of stacks of the given effect"""
        actor_effect = self.effects.get(effect_str, None)
        return actor_effect.stacks if actor_effect is not None else 0

    def negate_effect(self: AbstractActor, effect_str: str) -> int:
        """Remove the effect entirely and return the number of stacks removed."""
        actor_effect = self.effects.pop(effect_str, None)
        return actor_effect.stacks if actor_effect is not None else 0

    def decrease_effect(self, effect_str: str, quantity: int) -> int:
        """Decrease the stacks of this effect on the player by quantity. Return the stacks removed."""
        if effect_str not in self.effects:
            return 0
        return self.effects[effect_str].decrease_stacks(quantity)


    def clear_effects(self):
        self.effects.clear()

    def has_effect(self, effect, quantity=None):
        if quantity is None:
            return effect in self.effects
        else:
            return effect.stacks >= quantity

    def get_effect(self, effect) -> int:
        return self.effects.get(effect, 0)

    def set_effect(self, effect, value):
        self.effects[effect] = value

    def _apply(self: AbstractActor | AbstractEnemy, effect, quantity):
        if effect not in self.effects:
            self.effects[effect] = effect()
        self.effects[effect].increase_stacks(quantity)

    def _stack(self: AbstractActor | AbstractEnemy, effect_str: str, quantity: int):
        """Adds the effect to actor if missing and increases the stacks by quantity."""
        existing = self.effects.get(effect_str, None)
        self.effects[effect_str]

    def apply_all_effects(self: AbstractActor | AbstractEnemy, effects: list[tuple[str, int]]):
        for effect, quantity in effects:
            self._stack(effect, quantity)

    def apply_effect(self: AbstractActor | AbstractEnemy, effect: str, quantity: int):
        self._stack(effect, quantity)

    def apply_block(self: AbstractActor | AbstractEnemy, quantity: int):
        self._apply(Block, quantity)

    def apply_vulnerable(self: AbstractActor | AbstractEnemy, quantity: int):
        self._apply(Vulnerable, quantity)

    def apply_curlup(self: AbstractActor | AbstractEnemy, quantity: int):
        self._stack(CURLUP, quantity)

    def apply_strength(self: AbstractActor | AbstractEnemy, quantity: int):
        self._apply(Strength, quantity)

    def apply_ritual(self: AbstractActor | AbstractEnemy, quantity: int):
        self._apply(Ritual, quantity)
        self.ritual_flag = True
