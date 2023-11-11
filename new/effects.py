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
        print(damage)
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


class StrengthDown(AbstractEffect):

    def on_end_turn(self: AbstractEffect, owner: AbstractActor | AbstractEnemy):
        owner.decrease_effect(Strength, self.stacks)
        owner.set_effect(StrengthDown, 0)


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

    def process_effects(self: AbstractActor | AbstractEnemy, method_name: str, parameter=None):
        """
        This method streamlines the processing of effects by allowing you to quickly
        call a given method on all effects. It is
        """
        # Note: func = getattr(obj, method_name); func;
        # is essentially the same as doing obj.method_name()
        # This is somewhat brittle since we take method name as
        # a string, but I think it simplifies enough to be worth it
        # TODO: Only call on methods where it exists

        remove_effects = []
        for effect_name, effect in self.effects.items():
            func = getattr(self.effects.get(effect_name), method_name)
            if parameter:
                modification = func(parameter)
                parameter = parameter + modification
            else:
                func(self)
            if effect.stacks <= 0:
                remove_effects.append(effect_name)

        for i in range(len(remove_effects)):
            self.effects.pop(remove_effects[i])

        return parameter

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
            return effect.stacks >= quantity

    def _check_instantiate_effect(self, effect):
        if effect not in self.effects:
            self.effects[effect] = effect()

    def set_effect(self, effect, value):
        self._check_instantiate_effect(effect)
        self.effects.get(effect).stacks = value

    def increase_effect(self, effect, value):
        self._check_instantiate_effect(effect)
        self.effects.get(effect).stacks += value

    def decrease_effect(self, effect, value):
        self._check_instantiate_effect(effect)
        self.effects.get(effect).stacks -= value
