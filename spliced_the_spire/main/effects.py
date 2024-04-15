from __future__ import annotations

import math

from spliced_the_spire.main.enumerations import CardType

from spliced_the_spire.main.abstractions import AbstractActor, AbstractEnemy, AbstractEffect


class Energy(AbstractEffect):
    def __init__(self, owner):
        self.max = 3
        self.stacks = 3
        super().__init__(owner)

    def on_enter_combat(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment):
        self.stacks = self.max


class Dexterity(AbstractEffect):

    def on_gain_block_from_card(self, owner: AbstractActor | AbstractEnemy, environment, block):
        owner.increase_effect(Block, self.stacks)


class Thorns(AbstractEffect):

    def on_victim_of_attack(self, owner: AbstractActor | AbstractEnemy, environment,
                            damaging_enemy: AbstractEnemy):

        damaging_enemy.take_damage(damage=self.stacks)


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

        owner.decrease_effect(Block, blocked)
        return blocked * -1

    def on_start_turn(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment):
        if not owner.has_effect(BarricadeEffect):
            owner.set_effect(Block, 0)


class DoubleDamageForOneAttack(AbstractEffect):
    def modify_damage_dealt(self, owner, environment, damage: int) -> int:
        self.stacks = 0
        return damage * 2


class Vigor(AbstractEffect):
    def modify_damage_dealt(self, owner, environment, damage: int) -> int:
        add_damage = self.stacks
        self.stacks = 0
        return add_damage


class ThisBlockNextTurn(AbstractEffect):

    def on_start_turn(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment):
        owner.increase_effect(Block, self.stacks)
        self.stacks = 0


class ThisEnergyNextTurn(AbstractEffect):
    def on_start_turn(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment):
        owner.increase_effect(Energy, self.stacks)
        self.stacks = 0


class ThisStrengthNextTurn(AbstractEffect):

    def on_start_turn(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment):
        owner.increase_effect(Strength, self.stacks)
        self.stacks = 0


class Vulnerable(AbstractEffect):
    def on_end_turn(self, owner, environment):
        owner.decrease_effect(Vulnerable, 1)

    def modify_damage_taken(self, owner, environment, damage: int) -> int:
        # Vulnerable adds 50% damage
        return int(damage * .5)


class Strength(AbstractEffect):
    def modify_damage_dealt(self, owner, environment, damage: int) -> int:
        return 0 if not self.stacks else self.stacks


class Ritual(AbstractEffect):
    def on_end_turn(self, owner, environment):
        owner.increase_effect(Strength, 3)


class Weak(AbstractEffect):
    # TODO: Consider a "set_damage_dealt" method
    def modify_damage_dealt(self, owner, environment, damage: int):
        return (damage - math.floor(damage * 0.75)) * -1

    def on_end_turn(self: AbstractEffect, owner, environment):
        owner.decrease_effect(Weak, 1)


class StrengthDownAtEndOfTurn(AbstractEffect):

    def on_end_turn(self: AbstractEffect, owner, environment):
        owner.decrease_effect(Strength, self.stacks)
        owner.set_effect(StrengthDownAtEndOfTurn, 0)


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

    def on_victim_of_attack(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment, damaging_enemy):
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
    def on_victim_of_attack(self, owner, room, damaging_enemy):
        owner.increase_effect(Block, self.stacks)
        owner.set_effect(CurlUp, 0)


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

