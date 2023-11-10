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
        if self.stacks >= damage:
            blocked = damage
        else:
            blocked = self.stacks

        return blocked * -1

    def on_start_turn(self: AbstractEffect, owner: AbstractActor | AbstractEnemy):
        owner.set_effect(Block, 0)


class Vulnerable(AbstractEffect):
    def on_end_turn(self, owner: AbstractActor | AbstractEnemy):
        owner.decrease_effect(Vulnerable, 1)

    def modify_damage_taken(self, damage: int) -> int:
        # Vulnerable adds 50% damage
        return int(damage * .5)


class Strength(AbstractEffect):
    def modify_damage_dealt(self, damage: int) -> int:
        return self.stacks


class Ritual(AbstractEffect):
    def on_end_turn(self, owner: AbstractActor | AbstractEnemy):
        owner.increase_effect(Strength, 3)


class Weak(AbstractEffect):
    # TODO: Consider a "set_damage_dealt" method
    def modify_damage_dealt(self, damage: int):
        return (damage - math.floor(damage * 0.75)) * -1

    def on_end_turn(self: AbstractEffect, owner: AbstractActor | AbstractEnemy):
        owner.decrease_effect(Weak, 1)


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

    def has_effect(self, effect: type[AbstractEffect], quantity: int = None) -> bool:
        """
        This API has two behaviors depending on if the quantity value was specified or not.
        If the quantity was not specified, this will check if the player has any number of stacks
        of a given effect, and return true if they do. If the quantity value is specified however, this
        will only return true if the player has *at least* that number of stacks of the given effect.
        """
        if quantity is None:
            return effect in self.effects and self.effects.get(effect).stacks != 0
        else:
            return effect in self.effects and self.effects.get(effect).stacks >= quantity

    def stacks_of_effect(self, effect: type[AbstractEffect]) -> int:
        """Returns the current number of stacks of a given effect."""
        # If this effect hasn't been instantiated yet just return 0
        if effect not in self.effects:
            return 0

        # Otherwise, return the number of stacks
        return self.effects.get(effect).stacks

    def _check_instantiate_effect(self, effect):
        if effect not in self.effects:
            self.effects[effect] = effect()

    def set_effect(self, effect: type[AbstractEffect], value: int):
        """Set the number of stacks of this effect to the value provided."""
        self._check_instantiate_effect(effect)
        self.effects.get(effect).stacks = value

    def increase_effect(self, effect: type[AbstractEffect], value: int):
        """Increase the stacks of this effect by the value provided."""
        self._check_instantiate_effect(effect)
        self.effects.get(effect).stacks += value

    def decrease_effect(self, effect: type[AbstractEffect], value: int):
        """Decreases the stacks of this effect by the value provided."""
        self._check_instantiate_effect(effect)
        self.effects.get(effect).stacks -= value
