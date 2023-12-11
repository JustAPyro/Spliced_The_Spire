from __future__ import annotations

import math
from typing import TYPE_CHECKING

from new.enumerations import CardType

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

    def modify_damage_taken(self, owner, environment, damage: int) -> int:
        """
        Effects overriding this can modify the damage taken by an actor or enemy.
        The return value of this method will be added to the damage, you can lower the damage
        received by returning a negative value.
        """
        pass

    def modify_damage_dealt(self, owner, environment, damage: int) -> int:
        """
        Effects overriding this can modify the damage dealt by an actor or enemy.
        The return value of this method will be added to the damage, you can lower the damage
        dealt by returning a negative value.
        """
        pass

    def on_end_turn(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment):
        """
        Effects overriding this can cause things to happen on the end of turn.
        """
        pass

    def on_start_turn(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment):
        """
        Effects overriding this can cause things to happen on the end of turn.
        """
        pass

    def on_receive_damage_from_card(self: AbstractEffect, owner, environment, card):
        pass

    def on_card_play(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment, card):
        pass

    def on_card_draw(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment, card):
        pass

    def on_card_exhaust(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment):
        pass

    def on_take_damage(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment, damaging_enemy: AbstractEnemy):
        pass

    def modify_card_draw(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment, quantity):
        """
        Effects overriding this will modify the number of cards drawn
        """
        return 0


# =======================
# === Implementations ===
# =======================

class Block(AbstractEffect):
    def modify_damage_taken(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment, damage: int) -> int:
        if self.stacks >= damage:
            blocked = damage
        else:
            blocked = self.stacks

        environment['actor'].decrease_effect(Block, blocked)
        return blocked * -1

    def on_start_turn(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment):
        if not owner.has_effect(BarricadeEffect):
            owner.set_effect(Block, 0)


class Vulnerable(AbstractEffect):
    def on_end_turn(self, owner, environment):
        owner.decrease_effect(Vulnerable, 1)

    def modify_damage_taken(self, owner, environment, damage: int) -> int:
        # Vulnerable adds 50% damage
        return int(damage * .5)


class Strength(AbstractEffect):
    def modify_damage_dealt(self, owner, environment, damage: int) -> int:
        return self.stacks


class Ritual(AbstractEffect):
    def on_end_turn(self, owner, environment):
        owner.increase_effect(Strength, 3)


class Weak(AbstractEffect):
    # TODO: Consider a "set_damage_dealt" method
    def modify_damage_dealt(self, owner, environment, damage: int):
        return (damage - math.floor(damage * 0.75)) * -1

    def on_end_turn(self: AbstractEffect, owner, environment):
        owner.decrease_effect(Weak, 1)


class StrengthDown(AbstractEffect):

    def on_end_turn(self: AbstractEffect, owner, environment):
        owner.decrease_effect(Strength, self.stacks)
        owner.set_effect(StrengthDown, 0)


class NoDraw(AbstractEffect):
    def modify_card_draw(self, owner, environment, draw):
        return -1 * draw

    def on_end_turn(self: AbstractEffect, owner, environment):
        owner.set_effect(NoDraw, 0)


class CombustEffect(AbstractEffect):
    def on_end_turn(self: AbstractEffect, owner, environment):
        owner.health = owner.health - 1
        for enemy in environment['enemies']:
            enemy.health = enemy.health - self.stacks


class DarkEmbraceEffect(AbstractEffect):
    def on_card_exhaust(self: AbstractEffect, owner, environment):
        owner.draw_card(self.stacks)


class EvolveEffect(AbstractEffect):
    def on_card_draw(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment, card):
        if card.card_type == CardType.STATUS:
            owner.draw_card(self.stacks)


class FeelNoPainEffect(AbstractEffect):
    def on_card_exhaust(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment):
        owner.increase_effect(Block, self.stacks)


class FireBreathingEffect(AbstractEffect):
    def on_card_draw(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment, card):
        if card.card_type in (CardType.STATUS, CardType.CURSE):
            for enemy in environment['enemies']:
                enemy.health = enemy.health - self.stacks

class FlameBarrierEffect(AbstractEffect):

    def on_take_damage(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment, damaging_enemy):
        damaging_enemy.take_damage(self.stacks)


class MetallicizeEffect(AbstractEffect):
    def on_end_turn(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment):
        owner.increase_effect(Block, self.stacks)


class RageEffect(AbstractEffect):
    def on_card_play(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment, card):
        owner.increase_effect(Block, self.stacks)

    def on_end_turn(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment):
        owner.set_effect(RageEffect, 0)


class RuptureEffect(AbstractEffect):
    def on_receive_damage_from_card(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment, card):
        owner.increase_effect(Strength, self.stacks)


class BarricadeEffect(AbstractEffect):
    pass

class BerserkEffect(AbstractEffect):
    pass

class BrutalityEffect(AbstractEffect):
    pass

class CorruptionEffect(AbstractEffect):
    pass


class DemonFormEffect(AbstractEffect):
    pass


class DoubleTapEffect(AbstractEffect):
    pass

class JuggernautEffect(AbstractEffect):
    pass



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

    def process_effects(self: AbstractActor | AbstractEnemy, method_name: str, environment, parameter=None):
        """
        This method streamlines the processing of effects by allowing you to quickly
        call a given method on all effects. It is
        """
        # Note: func = getattr(obj, method_name); func;
        # is essentially the same as doing obj.method_name()
        # This is somewhat brittle since we take method name as
        # a string, but I think it simplifies enough to be worth it
        # TODO: Only call on methods where it exists

        for effect_name in list(self.effects):
            func = getattr(self.effects.get(effect_name), method_name)
            if parameter is not None:
                # Bug here?
                modification = func(self.effects.get(effect_name), environment, parameter)
                if modification is not None:
                    parameter = parameter + modification
            else:
                func(self, environment)
            for effect in list(self.effects):
                if self.effects.get(effect).stacks <= 0:
                    self.effects.pop(effect)

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

    def get_effect_stacks(self, effect):
        self._check_instantiate_effect(effect)
        return self.effects.get(effect).stacks
