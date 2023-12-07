import random
from abc import ABC, abstractmethod
from copy import deepcopy

from typing import TYPE_CHECKING
from enum import Enum

from new import effects
from new.effects import *
from new.enumerations import CardType, SelectEvent, CardPiles

if TYPE_CHECKING:
    from actors import AbstractActor
    from enemies import AbstractEnemy


class AbstractCard(ABC):
    """
    Abstract card class is the blueprint for all cards. The goal for this class
    is to allow simple, quick implementation of Slay the Spire cards. To use write an implementation
    for a card, write a class that inherits this class as well as ABC, then implement an __init__,
    use, and upgrade_logic methods.
    """

    def __init__(self,
                 energy_cost: int,
                 card_type: CardType,
                 upgraded: bool = False,
                 name: str = None,
                 exhaust: bool = False,
                 ethereal: bool = False,
                 allow_multiple_upgrades: bool = False):
        # Name of the card
        if name is None:
            class_name = type(self).__name__
            final_name = ''

            for char in class_name:
                if char.isupper():
                    final_name += ' '
                final_name += char
            self.name: str = final_name[1:]
        else:
            self.name: str = name

        # normal energy cost of card ("cost" int)
        self.energy_cost: int = energy_cost
        self.ex_energy_cost: int = -1

        # If the card is upgraded or not
        self.upgraded: bool = upgraded

        # Type of card
        self.card_type: CardType = card_type

        # Card behavior
        self.exhaust: bool = exhaust
        self.ethereal: bool = ethereal
        self.poof: bool = False

        self.allow_multiple_upgrades = allow_multiple_upgrades

        # Setup for power type cards
        if self.card_type is CardType.POWER:
            self.poof = True
            if self.exhaust or self.ethereal:
                raise RuntimeError('WAT? (Power card with exhaust/ethereal found)')

    # --- Card Cost API ---
    def modify_cost_this_turn(self, cost: int):
        self.ex_energy_cost = self.energy_cost
        self.energy_cost = cost


    @abstractmethod
    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        """Overriding this method provides the default behavior of a card."""
        pass

    def upgrade(self):
        if self.upgraded and not self.allow_multiple_upgrades:
            return

        if not self.upgraded:
            self.name = self.name + "+"
        self.upgraded = True
        self.upgrade_logic()

    @abstractmethod
    def upgrade_logic(self):
        """Overriding this method provides the behavior of the card on upgrade."""
        pass

    def is_playable(self, caller):
        return True

    def cost(self, actor):
        return self.energy_cost

    # Override the str() method so printing it returns the name
    def __str__(self):
        return self.name

    # Override the repr() method so arrays print neatly
    def __repr__(self):
        return self.name


class Wound(AbstractCard, ABC):
    def __init__(self):
        super().__init__(name='Wound', energy_cost=0, card_type=CardType.STATUS)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass

    def is_playable(self, caller):
        return False


class Dazed(AbstractCard, ABC):
    def __init__(self):
        super().__init__(name='Dazed', energy_cost=0, card_type=CardType.STATUS, ethereal=True)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass

    def is_playable(self, caller):
        return False


class RedStrike(AbstractCard, ABC):
    def __init__(self):
        self.damage = 6
        super().__init__(name='Strike', energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)

    def upgrade_logic(self):
        self.damage = 9


class RedDefend(AbstractCard, ABC):
    def __init__(self):
        self.block = 5
        super().__init__(name='Defend', energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(Block, self.block)

    def upgrade_logic(self):
        self.block = 8


class Bash(AbstractCard, ABC):
    def __init__(self):
        self.damage = 8
        self.vulnerable = 2
        super().__init__(energy_cost=2, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)
        target.increase_effect(Vulnerable, self.vulnerable)

    def upgrade_logic(self):
        self.damage = 10
        self.vulnerable = 3


class Anger(AbstractCard, ABC):
    def __init__(self):
        self.damage = 6
        super().__init__(energy_cost=0, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)
        caller.discard_pile.append(Anger())

    def upgrade_logic(self):
        self.damage = 8


class Armaments(AbstractCard, ABC):
    def __init__(self):
        self.block = 5
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller, target, environment):
        caller.increase_effect(Block, self.block)
        if self.upgraded:
            for card in caller.hand_pile:
                card.upgrade()
            return
        caller.hand_pile.remove(self)
        random.choice(caller.get_hand()).upgrade()
        caller.hand_pile.append(self)

    def upgrade_logic(self):
        pass


class BodySlam(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        if caller.effects.get(Block):
            caller.deal_damage(target, caller.get_effect_stacks(Block))

    def upgrade_logic(self):
        self.energy_cost = 0


class Clash(AbstractCard, ABC):

    def __init__(self):
        self.damage = 14
        super().__init__(energy_cost=0, card_type=CardType.ATTACK)

    def use(self, caller, target, environment):
        caller.deal_damage(target, self.damage)

    def upgrade_logic(self):
        self.damage = 18

    def is_playable(self, caller):
        for card in caller.get_hand():
            if card.card_type != CardType.ATTACK:
                return False
        return True


class Cleave(AbstractCard, ABC):
    def __init__(self):
        self.damage = 8
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller, target, environment):
        for enemy in environment['enemies']:
            caller.deal_damage(enemy, self.damage)

    def upgrade_logic(self):
        self.damage = 11


class Clothesline(AbstractCard, ABC):
    def __init__(self):
        self.damage = 12
        self.qty_weak = 2
        super().__init__(energy_cost=2, card_type=CardType.ATTACK)

    # TODO: make caller.take_damage a mangled method
    def use(self, caller, target, environment):
        caller.deal_damage(target, self.damage)
        target.increase_effect(Weak, self.qty_weak)

    def upgrade_logic(self):
        self.damage = 14
        self.qty_weak = 3


class Flex(AbstractCard, ABC):
    def __init__(self):
        self.strength_amount = 2
        super().__init__(energy_cost=0, card_type=CardType.SKILL)

    def use(self, caller, target, environment):
        caller.increase_effect(Strength, self.strength_amount)
        caller.increase_effect(StrengthDown, self.strength_amount)

    def upgrade_logic(self):
        self.strength_amount = 4


class Havoc(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller, target, environment):
        did_we_draw_card = caller.draw_card(1)
        if did_we_draw_card:
            caller.use_card(target, caller.hand_pile[-1], environment['enemies'], is_free=True, will_discard=False)
            caller.exhaust_card(caller.hand_pile[-1])

    def upgrade_logic(self):
        self.energy_cost = 0


class Headbutt(AbstractCard, ABC):
    def __init__(self):
        self.damage = 9
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller, target, environment):
        caller.deal_damage(target, self.damage)

        if caller.discard_pile:
            card = caller.select_card(caller.discard_pile)
            caller.draw_pile.append(card)
            caller.discard_pile.remove(card)

    def upgrade_logic(self):
        self.damage = 12


class HeavyBlade(AbstractCard, ABC):
    def __init__(self):
        self.extra_strength_multiplier = 3
        super().__init__(energy_cost=2, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, 14 + (caller.get_effect_stacks(Strength) * (self.extra_strength_multiplier - 1)))

    def upgrade_logic(self):
        self.extra_strength_multiplier = 5


class IronWave(AbstractCard, ABC):
    def __init__(self):
        self.damage = 5
        self.block = 5
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)
        caller.increase_effect(Block, self.block)

    def upgrade_logic(self):
        self.damage = 7
        self.block = 7


class PerfectedStrike(AbstractCard, ABC):
    def __init__(self):
        self.base_damage = 6
        self.increase = 2
        super().__init__(energy_cost=2, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        damage = self.base_damage
        for card in caller.get_combat_deck():
            if 'Strike' in card.name:
                damage += self.increase
        caller.deal_damage(target, damage)

    def upgrade_logic(self):
        self.increase = 3


class PommelStrike(AbstractCard, ABC):
    def __init__(self):
        self.damage = 9
        self.draw = 1
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)
        caller.draw_card(self.draw)

    def upgrade_logic(self):
        self.damage = 10
        self.draw = 2


class ShrugItOff(AbstractCard, ABC):
    def __init__(self):
        self.block = 8
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(Block, self.block)
        caller.draw_card(1)

    def upgrade_logic(self):
        self.block = 11


class SwordBoomerang(AbstractCard, ABC):
    def __init__(self):
        self.damage_times = 3
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        for _ in range(self.damage_times):
            caller.deal_damage(random.choice(environment['enemies']), 3)

    def upgrade_logic(self):
        self.damage_times = 4


##########################
######################TODO
##########################

class Thunderclap(AbstractCard, ABC):
    def __init__(self):
        self.damage = 4
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        for enemy in environment['enemies']:
            caller.deal_damage(enemy, self.damage)
            caller.increase_effect(Vulnerable, 1)

    def upgrade_logic(self):
        self.damage = 7


class TrueGrit(AbstractCard, ABC):
    def __init__(self):
        self.block = 7
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(Block, self.block)
        if self.upgraded:
            caller.exhaust_card(caller.select_card(caller.get_hand_without(self), SelectEvent.EXHAUST))
        else:
            caller.exhaust_card(random.choice(caller.hand_pile))

    def upgrade_logic(self):
        self.block = 9


class TwinStrike(AbstractCard, ABC):
    def __init__(self):
        self.damage = 5
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

        for _ in range(2):
            caller.deal_damage(target, self.damage)

    def upgrade_logic(self):
        self.damage = 7


class Warcry(AbstractCard, ABC):
    def __init__(self):
        self.draw_num = 1
        super().__init__(energy_cost=0, card_type=CardType.SKILL, exhaust=True)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.draw_card(self.draw_num)
        caller.draw_pile.append(caller.select_card(caller.get_hand_without(self), SelectEvent.PLACE_ON_DRAWPILE))

    def upgrade_logic(self):
        self.draw_num = 2


class WildStrike(AbstractCard, ABC):
    def __init__(self):
        self.damage = 12
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)
        caller.add_card_to_draw(Wound(), shuffle=True)

    def upgrade_logic(self):
        self.damage = 17


class BattleTrance(AbstractCard, ABC):
    def __init__(self):
        self.draw_qty = 3
        super().__init__(energy_cost=0, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.draw_card(self.draw_qty)
        caller.set_effect(NoDraw, 1)

    def upgrade_logic(self):
        self.draw_qty = 4


class BloodForBlood(AbstractCard, ABC):
    def __init__(self):
        self.damage = 18
        super().__init__(energy_cost=4, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)

    def upgrade_logic(self):
        self.energy_cost = 3
        self.damage = 22

    def cost(self, actor):
        return self.energy_cost - actor.times_received_damage


class Bloodletting(AbstractCard, ABC):
    def __init__(self):
        self.energy_gain = 2
        super().__init__(energy_cost=0, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.receive_damage_from_card(3, self)
        caller.energy = caller.energy + self.energy_gain

    def upgrade_logic(self):
        self.energy_gain = 3


class BurningPact(AbstractCard, ABC):
    def __init__(self):
        self.card_draw = 2
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.draw_card(self.card_draw)
        caller.exhaust_card(caller.select_card(caller.get_hand_without(self), SelectEvent.EXHAUST))

    def upgrade_logic(self):
        self.card_draw = 3


class Carnage(AbstractCard, ABC):
    def __init__(self):
        self.damage = 20
        super().__init__(energy_cost=2, card_type=CardType.ATTACK, ethereal=True)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)

    def upgrade_logic(self):
        self.damage = 28


class Combust(AbstractCard, ABC):
    def __init__(self):
        self.stacks = 5
        super().__init__(energy_cost=1, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(effects.CombustEffect, self.stacks)

    def upgrade_logic(self):
        self.stacks = 7


class DarkEmbrace(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=2, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(DarkEmbraceEffect, 1)

    def upgrade_logic(self):
        self.energy_cost = 1


class Disarm(AbstractCard, ABC):
    def __init__(self):
        self.strength_loss = 2
        super().__init__(energy_cost=1, card_type=CardType.SKILL, exhaust=True)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        target.decrease_effect(Strength, self.strength_loss)

    def upgrade_logic(self):
        self.strength_loss = 3


class Dropkick(AbstractCard, ABC):
    def __init__(self):
        self.damage = 5
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)
        if target.has_effect(Vulnerable):
            caller.gain_energy()
            caller.draw_card()

    def upgrade_logic(self):
        self.damage = 8


class DuelWield(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        # Have the actor select a valid card
        card = caller.select_card(
            event_type=SelectEvent.COPY,
            options=caller.get_cards(
                from_piles=[CardPiles.HAND],
                card_types=[CardType.ATTACK, CardType.POWER]))

        # Add one to hand
        caller.add_card_to_hand(deepcopy(card))

        # And if upgraded add a second
        if self.upgraded:
            caller.add_card_to_hand(deepcopy(card))

    def upgrade_logic(self):
        pass


class Entrench(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=2, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(Block, caller.get_effect_stacks(Block))

    def upgrade_logic(self):
        self.energy_cost = 1


class Evolve(AbstractCard, ABC):
    def __init__(self):
        self.draw = 1
        super().__init__(energy_cost=1, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(EvolveEffect, self.draw)

    def upgrade_logic(self):
        self.draw = 2


class FeelNoPain(AbstractCard, ABC):
    def __init__(self):
        self.block = 3
        super().__init__(energy_cost=1, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(FeelNoPainEffect, self.block)

    def upgrade_logic(self):
        self.block = 4


class Firebreathing(AbstractCard, ABC):
    def __init__(self):
        self.damage = 6
        super().__init__(energy_cost=1, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(FireBreathingEffect, self.damage)

    def upgrade_logic(self):
        self.damage = 10


class FlameBarrier(AbstractCard, ABC):
    def __init__(self):
        self.damage = 4
        super().__init__(energy_cost=2, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(FlameBarrierEffect, self.damage)

    def upgrade_logic(self):
        self.damage = 6


class GhostlyArmor(AbstractCard, ABC):
    def __init__(self):
        self.block = 10
        super().__init__(energy_cost=1, card_type=CardType.SKILL, ethereal=True)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(Block, self.block)

    def upgrade_logic(self):
        self.block = 13


class Hemokinesis(AbstractCard, ABC):
    def __init__(self):
        self.damage = 15
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(self.damage)
        caller.receive_damage_from_card(2, self)

    def upgrade_logic(self):
        self.damage = 20


class InfernalBlade(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.SKILL, exhaust=True)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        card_cls = random.choice([subclass for subclass in AbstractCard.__subclasses__()
                                  if subclass().card_type == CardType.ATTACK
                                  and subclass not in (Feed, Reaper)])
        card = card_cls()
        card.modify_cost_this_turn(0)
        caller.add_card_to_hand(card)

    def upgrade_logic(self):
        self.energy_cost = 0


class Inflame(AbstractCard, ABC):
    def __init__(self):
        self.str = 2
        super().__init__(energy_cost=1, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(Strength, self.str)

    def upgrade_logic(self):
        self.str = 3


class Intimidate(AbstractCard, ABC):
    def __init__(self):
        self.weak = 1
        super().__init__(energy_cost=0, card_type=CardType.SKILL, exhaust=True)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        for enemy in environment['enemies']:
            enemy: AbstractEnemy
            enemy.increase_effect(Weak, self.weak)

    def upgrade_logic(self):
        self.weak = 2


class Metallicize(AbstractCard, ABC):
    def __init__(self):
        self.metal = 3
        super().__init__(energy_cost=1, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(MetallicizeEffect, self.metal)

    def upgrade_logic(self):
        self.metal = 4


class PowerThrough(AbstractCard, ABC):
    def __init__(self):
        self.block_qty = 15
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.add_card_to_hand(Wound)
        caller.add_card_to_hand(Wound)
        caller.increase_effect(Block, self.block_qty)

    def upgrade_logic(self):
        self.block_qty = 20


class Pummel(AbstractCard, ABC):
    def __init__(self):
        self.times = 4
        super().__init__(energy_cost=1, card_type=CardType.ATTACK, exhaust=True)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        for i in range(self.times):
            caller.deal_damage(target, 4)

    def upgrade_logic(self):
        self.times = 5


class Rage(AbstractCard, ABC):
    def __init__(self):
        self.stack_qty = 3
        super().__init__(energy_cost=0, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(RageEffect, self.stack_qty)

    def upgrade_logic(self):
        self.stack_qty = 5


class Rampage(AbstractCard, ABC):
    def __init__(self):
        self.damage = 8
        self.upgrade_amount = 5
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)
        self.damage += self.upgrade_amount

    def upgrade_logic(self):
        self.upgrade_amount = 8


class RecklessCharge(AbstractCard, ABC):
    def __init__(self):
        self.damage = 7
        super().__init__(energy_cost=0, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)
        caller.add_card_to_draw(Dazed, shuffle=True)

    def upgrade_logic(self):
        self.damage = 10


class Rupture(AbstractCard, ABC):
    def __init__(self):
        self.strength = 1
        super().__init__(energy_cost=1, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(RuptureEffect, self.strength)

    def upgrade_logic(self):
        self.strength = 2


class SearingBlow(AbstractCard, ABC):
    def __init__(self):
        self.upgraded_qty = 0
        super().__init__(energy_cost=2, card_type=CardType.ATTACK, allow_multiple_upgrades=True)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, 12 + (4 * self.upgraded_qty))

    def upgrade_logic(self):
        self.upgraded_qty += 1


class SecondWind(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass


class SeeingRed(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass


class Sentinel(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass


class SeverSoul(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=2, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass


class Shockwave(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=2, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass


class SpotWeakness(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass


class Uppercut(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=2, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass


class Whirlwind(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost='x', card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass


class Barricade(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=3, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass


class Berserk(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=0, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass


class Bludgeon(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=3, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass


class Brutality(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=0, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass


class Corruption(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=3, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass


class DemonForm(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=3, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass


class DoubleTap(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass


class Exhume(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass


class Feed(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass


class FiendFire(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=2, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass


class Immolate(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=2, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass


class Impervious(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=2, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass


class Juggernaut(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=2, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass


class LimitBreak(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass


class Offering(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=0, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass


class Reaper(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=2, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass
