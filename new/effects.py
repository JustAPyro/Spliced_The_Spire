from __future__ import annotations

import math
from typing import TYPE_CHECKING

from new.enumerations import CardType

if TYPE_CHECKING:
    from new.abstractions import AbstractActor, AbstractEffect
    from enemies import AbstractEnemy


# =======================
# === Implementations ===
# =======================

class Poison(AbstractEffect):
    def on_end_turn(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment):
        owner.take_damage(self.stacks)
        if self.stacks > 0:
            owner.decrease_effect(Poison, 1)


class Block(AbstractEffect):
    def modify_damage_taken(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment,
                            damage: int) -> int:
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


class CurlUp(AbstractEffect):
    pass


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



