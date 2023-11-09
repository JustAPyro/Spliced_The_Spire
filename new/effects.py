from __future__ import annotations

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from actors import AbstractActor
    from enemies import AbstractEnemy


# ===================
# === Abstraction ===
# ===================

class AbstractEffect:
    """
    This abstraction allows the easy creation of Effects.
    An effect in this context is a Slay The Spire Buff,
    Debuff, or block.
    """

    def __init__(self):
        self.stacks = 0  # Number of stacks of this effect

    def decrease_stacks(self: AbstractEffect, quantity: int = 1) -> int:
        """Decrease the number of stacks of this effect by quantity. Return the number removed."""

        # If this resulted in negative set to 0
        # And say we removed however many existed
        if self.stacks - quantity < 0:
            removed = self.stacks
            self.stacks = 0
            return removed

        # Otherwise we reduce it by quantity
        # and return that
        self.stacks = self.stacks - quantity
        return quantity

    def increase_stacks(self: AbstractEffect, quantity: int = 1):
        """Increase the number of stacks of this effect by quantity."""
        self.stacks += quantity

    # === API/SANDBOX METHODS ===

    def modify_damage_taken(self, damage: int) -> int:
        """
        Effects overriding this can modify the damage taken by an actor or enemy.
        The return value of this method will be added to the damage, you can lower the damage
        received by returning a negative value.
        """
        pass

    def modify_damage_dealt(self, damage: int) -> int:
        """
            Effects overriding this can modify the damage dealt by an actor or enemy.
            The return value of this method will be added to the damage, you can lower the damage
            dealt by returning a negative value.
        """
        pass

    def on_end_turn(self: AbstractEffect, owner: AbstractActor | AbstractEnemy):
        """
        Effects overriding this can cause things to happen on the end of turn.
        """
        pass

    def on_start_turn(self: AbstractEffect, owner: AbstractActor | AbstractEnemy):
        """
        Effects overriding this can cause things to happen on the end of turn.
        """
        pass


# =======================
# === Implementations ===
# =======================

class Block(AbstractEffect):
    def modify_damage_taken(self: AbstractEffect, damage: int) -> int:
        # This tries to decrease the number of block by the damage,
        # and returns how many block were actually removed
        stacks_removed = self.decrease_stacks(damage)

        # To modify damage by the number of stacks we return the
        # negative of that
        return -1 * stacks_removed

    def on_start_turn(self: AbstractEffect, owner: AbstractActor | AbstractEnemy):
        owner.set_effect(Block, 0)


class Vulnerable(AbstractEffect):
    def on_end_turn(self, owner: AbstractActor | AbstractEnemy):
        owner.apply_vulnerable(-1)

    def modify_damage_taken(self, damage: int) -> int:
        # Vulnerable adds 50% damage
        return int(damage * .5)


class Strength(AbstractEffect):
    def modify_damage_dealt(self, damage: int) -> int:
        return self.stacks


class Ritual(AbstractEffect):
    def on_end_turn(self, owner: AbstractActor | AbstractEnemy):
        owner.apply_strength(self.stacks)


class Weak(AbstractEffect):
    # TODO: Consider a "set_damage_dealt" method
    def modify_damage_dealt(self, damage: int):
        return (damage - math.floor(damage * 0.75)) * -1


# ===================================
# === Effect Management and Mixin ===
# ===================================

class EffectMixin:
    """
    This EffectMixin class is added to both the actors and the enemies, and allows for
    managing different effects.

    Below are listed common API methods you are encouraged to use in the development
    of cards, enemies, relics, and effects. (Note that entity in this case means a player
    or enemy)

    - entity.clear_effects() -> Remove all effects from an entity
    - entity.add_effects(effect, qty) -> increments stacks of effect by qty
    - entity.set_effects(effect, qty) -> sets the stacks of effect to qty
    - entity.has_effect(effect) -> Returns true if entity has effect
    - entity.has_effect(effect, qty) -> returns true if entity has at least qty stacks of effect
    - entity.get_stacks(effect) -> Returns the number of stacks of effect
    """

    def __init__(self):
        # This is the primary dictionary of effects on an entity
        self.effects: dict[type[AbstractEffect], AbstractEffect] = {}
        self.ritual_flag: bool = False

    def process_effects(self: AbstractActor | AbstractEnemy, method_name: str):
        """
        This method streamlines the processing of effects by allowing you to quickly
        call a given method on all effects. It is
        """
        for effect in list(self.effects):
            # Note: func = getattr(obj, method_name); func;
            # is essentially the same as doing obj.method_name()
            # This is somewhat brittle since we take method name as
            # a string, but I think it simplifies enough to be worth it
            # TODO: Only call on methods where it exists
            func = getattr(self.effects.get(effect), method_name)
            func(self)

    def get_effects_dict(self) -> dict[str, int]:
        """
        Returns a dictionary of effects in the format {"effect name": stacks}
        This is primarily used for displaying information about all the stacks on an entity.
        """
        # Start with an empty dictionary
        effects_dict = {}
        for effect in self.effects:
            # Add a dictionary entry using the name of the effect as key and stacks as qty
            effects_dict[effect.__name__] = self.effects[effect].stacks
        # Return the final dict
        return effects_dict

    def clear_effects(self):
        """
        Removes all effects from the owner.
        """
        self.effects.clear()

    def has_effect(self, effect, quantity=None):
        if quantity is None:
            return effect in self.effects
        else:
            return self.effect.get >= quantity

    def set_effect(self, effect, value):
        self.effects.get(effect).stacks = value

    def _apply(self: AbstractActor | AbstractEnemy, effect, quantity):
        if effect not in self.effects:
            self.effects[effect] = effect()
        self.effects[effect].increase_stacks(quantity)

    def apply_effect(self: AbstractActor | AbstractEnemy, effect: type[AbstractEffect], quantity: int):
        self._apply(effect, quantity)

    def apply_block(self: AbstractActor | AbstractEnemy, quantity: int):
        self._apply(Block, quantity)

    def apply_vulnerable(self: AbstractActor | AbstractEnemy, quantity: int):
        self._apply(Vulnerable, quantity)

    def apply_strength(self: AbstractActor | AbstractEnemy, quantity: int):
        self._apply(Strength, quantity)

    def apply_ritual(self: AbstractActor | AbstractEnemy, quantity: int):
        self._apply(Ritual, quantity)
        self.ritual_flag = True
