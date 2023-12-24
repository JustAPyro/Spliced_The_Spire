from __future__ import annotations

import random
from abc import ABC
from copy import deepcopy
from itertools import product
from spliced_the_spire.new import effects
from spliced_the_spire.new.effects import *
from spliced_the_spire.new.enumerations import CardType, SelectEvent, CardPiles, IntentType, Color, Rarity

from spliced_the_spire.new.abstractions import *


################
# STATUS CARDS #
################
# https://slay-the-spire.fandom.com/wiki/Status
# Burn, Dazed, Wound, Slimed, Void,

class Burn(AbstractCard, ABC):
    pass


class Dazed(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(name='Dazed', energy_cost=0, card_type=CardType.STATUS, ethereal=True)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass

    def is_playable(self, caller):
        return False


class Wound(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(name='Wound', energy_cost=0, card_type=CardType.STATUS)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

    def upgrade_logic(self):
        pass

    def is_playable(self, caller):
        return False


# Silent cards
class GreenStrike(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 6
        super().__init__(name='Strike', energy_cost=1, card_type=CardType.ATTACK,
                         card_color=Color.GREEN, card_rarity=Rarity.STARTER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)

    def upgrade_logic(self):
        self.damage = 9


class GreenDefend(AbstractCard, ABC):
    sts_name = 'Defend_G'

    def __init__(self, *args, **kwargs):
        self.block = 5
        super().__init__(name='Defend', energy_cost=1, card_type=CardType.SKILL,
                         card_rarity=Rarity.STARTER, card_color=Color.GREEN)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(Block, self.block)

    def upgrade_logic(self):
        self.block = 8


class Neutralize(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 3
        self.weak = 1
        super().__init__(name='Neutralize', energy_cost=0, card_type=CardType.ATTACK,
                         card_rarity=Rarity.STARTER, card_color=Color.GREEN)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)
        target.increase_effect(Weak, self.weak)

    def upgrade_logic(self):
        self.damage = 4
        self.weak = 2


class Survivor(AbstractCard, ABC):

    def __init__(self, *args, **kwargs):
        self.block = 8
        super().__init__(name='Survivor', energy_cost=1, card_type=CardType.SKILL,
                         card_rarity=Rarity.STARTER, card_color=Color.GREEN)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(Block, self.block)
        chosenDiscard = caller.select_card(caller.get_hand(), event_type=SelectEvent.DISCARD)
        caller.discard_card(chosenDiscard)

    def upgrade_logic(self):
        self.block = 11


class Acrobatics(AbstractCard, ABC):

    def __init__(self, *args, **kwargs):
        self.cardDraw = 3
        super().__init__(name='Acrobatics', energy_cost=1, card_type=CardType.SKILL,
                         card_rarity=Rarity.COMMON, card_color=Color.GREEN)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.draw_card(quantity=self.cardDraw)
        chosenDiscard = caller.select_card(caller.get_hand(), event_type=SelectEvent.DISCARD)
        caller.discard_card(chosenDiscard)

    def upgrade_logic(self):
        self.cardDraw = 4


class Backflip(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.block = 5
        self.draw = 2
        super().__init__(name='Backflip', energy_cost=1, card_type=CardType.SKILL,
                         card_rarity=Rarity.COMMON, card_color=Color.GREEN)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(Block, self.block)
        caller.draw_card(quantity=self.draw)

    def upgrade_logic(self):
        self.block = 8


class Bane(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 7
        super().__init__(name='Bane', energy_cost=1, card_type=CardType.ATTACK,
                         card_rarity=Rarity.COMMON, card_color=Color.GREEN)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        target.take_damage(self.damage)
        if target.has_effect(Poison):
            target.take_damage(self.damage)

    def upgrade_logic(self):
        self.damage = 10


class Shiv(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 4
        super().__init__(name='Shiv',
                         energy_cost=0,
                         card_type=CardType.ATTACK,
                         exhaust=True,
                         card_rarity=Rarity.SPECIAL,
                         card_color=Color.COLORLESS,
                         remove_after_combat=True)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        target.take_damage(self.damage)

    def upgrade_logic(self):
        self.damage = 6


class CloakAndDagger(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1,
                         card_type=CardType.SKILL,
                         card_rarity=Rarity.COMMON,
                         card_color=Color.GREEN)

        self.numberOfDaggers = 1

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(Block, 6)
        for i in range(self.numberOfDaggers):
            caller.add_card_to_hand(Shiv())

    def upgrade_logic(self):
        self.numberOfDaggers = 2


class DaggerSpray(AbstractCard, ABC):

    def __init__(self):
        super(DaggerSpray, self).__init__(energy_cost=1,
                                          card_rarity=Rarity.COMMON,
                                          card_type=CardType.ATTACK,
                                          card_color=Color.GREEN)
        self.damage = 4

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment: AbstractCombat):
        for i in range(2):

            for enemy in environment.enemies:
                enemy.take_damage(self.damage)

    def upgrade_logic(self):
        self.damage = 6


class DaggerThrow(AbstractCard, ABC):
    def __init__(self):
        super(DaggerThrow, self).__init__(energy_cost=1,
                                          card_rarity=Rarity.COMMON,
                                          card_type=CardType.ATTACK,
                                          card_color=Color.GREEN)
        self.damage = 9

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        target.take_damage(self.damage)
        caller.draw_card(1)
        caller.select_card(caller.get_hand(), SelectEvent.DISCARD)

    def upgrade_logic(self):
        self.damage = 12


class DeadlyPoison(AbstractCard, ABC):
    def __init__(self):
        super(DeadlyPoison, self).__init__(energy_cost=1,
                                           card_rarity=Rarity.COMMON,
                                           card_type=CardType.SKILL,
                                           card_color=Color.GREEN)
        self.poisonAmount = 5

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        target.increase_effect(Poison, self.poisonAmount)

    def upgrade_logic(self):
        self.poisonAmount = 7


class Deflect(AbstractCard, ABC):
    def __init__(self):
        super(Deflect, self).__init__(energy_cost=0,
                                      card_rarity=Rarity.COMMON,
                                      card_type=CardType.SKILL,
                                      card_color=Color.GREEN)
        self.block = 4

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(Block, self.block)

    def upgrade_logic(self):
        self.block = 7


class DodgeAndRoll(AbstractCard, ABC):
    def __init__(self):
        super(DodgeAndRoll, self).__init__(energy_cost=1,
                                           card_rarity=Rarity.COMMON,
                                           card_type=CardType.SKILL,
                                           card_color=Color.GREEN)
        self.block = 4

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(Block, self.block)
        caller.increase_effect(ThisBlockNextTurn, self.block)

    def upgrade_logic(self):
        self.block = 6


class FlyingKnee(AbstractCard, ABC):
    def __init__(self):
        super(FlyingKnee, self).__init__(energy_cost=1,
                                         card_rarity=Rarity.COMMON,
                                         card_type=CardType.ATTACK,
                                         card_color=Color.GREEN)
        self.damage = 8

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        target.take_damage(self.damage)
        caller.increase_effect(ThisEnergyNextTurn, 1)

    def upgrade_logic(self):
        self.damage = 11


class Outmaneuver(AbstractCard, ABC):
    def __init__(self):
        super(Outmaneuver, self).__init__(energy_cost=1,
                                          card_rarity=Rarity.COMMON,
                                          card_type=CardType.SKILL,
                                          card_color=Color.GREEN)
        self.energy = 2

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(ThisEnergyNextTurn, self.energy)

    def upgrade_logic(self):
        self.energy = 3


class PiercingWail(AbstractCard, ABC):
    def __init__(self):
        super(PiercingWail, self).__init__(energy_cost=1,
                                           card_rarity=Rarity.COMMON,
                                           card_type=CardType.SKILL,
                                           card_color=Color.GREEN,
                                           exhaust=True)
        self.amountStrength = 6

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        for enemy in environment.enemies:
            enemy.increase_effect(ThisStrengthNextTurn, self.amountStrength)
            enemy.increase_effect(Strength, self.amountStrength * -1)

    def upgrade_logic(self):
        self.amountStrength = 8




# Ironclad cards
class RedStrike(AbstractCard, ABC):
    sts_name = 'Strike_R'

    def __init__(self, *args, **kwargs):
        self.damage = 6
        super().__init__(name='Strike', energy_cost=1, card_type=CardType.ATTACK,
                         card_rarity=Rarity.STARTER, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)

    def upgrade_logic(self):
        self.damage = 9


class RedDefend(AbstractCard, ABC):
    sts_name = 'Defend_R'

    def __init__(self, *args, **kwargs):
        self.block = 5
        super().__init__(name='Defend', energy_cost=1, card_type=CardType.SKILL,
                         card_rarity=Rarity.STARTER, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(Block, self.block)

    def upgrade_logic(self):
        self.block = 8


class Bash(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 8
        self.vulnerable = 2
        super().__init__(energy_cost=2, card_type=CardType.ATTACK,
                         card_rarity=Rarity.STARTER, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)
        target.increase_effect(Vulnerable, self.vulnerable)

    def upgrade_logic(self):
        self.damage = 10
        self.vulnerable = 3


class Anger(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 6
        super().__init__(energy_cost=0, card_type=CardType.ATTACK,
                         card_rarity=Rarity.COMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)
        caller.discard_pile.append(Anger())

    def upgrade_logic(self):
        self.damage = 8


class Armaments(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.block = 5
        super().__init__(energy_cost=1, card_type=CardType.SKILL,
                         card_rarity=Rarity.COMMON, card_color=Color.RED,
                         *args, **kwargs)

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
    def __init__(self, *args, **kwargs):
        super().__init__(energy_cost=1, card_type=CardType.ATTACK,
                         card_rarity=Rarity.COMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        if caller.effects.get(Block):
            caller.deal_damage(target, caller.get_effect_stacks(Block))

    def upgrade_logic(self):
        self.energy_cost = 0


class Clash(AbstractCard, ABC):

    def __init__(self, *args, **kwargs):
        self.damage = 14
        super().__init__(energy_cost=0, card_type=CardType.ATTACK,
                         card_rarity=Rarity.COMMON, card_color=Color.RED,
                         *args, **kwargs)

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
    def __init__(self, *args, **kwargs):
        self.damage = 8
        super().__init__(energy_cost=1, card_type=CardType.ATTACK,
                         card_rarity=Rarity.COMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller, target, environment):
        for enemy in environment['enemies']:
            caller.deal_damage(enemy, self.damage)

    def upgrade_logic(self):
        self.damage = 11


class Clothesline(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 12
        self.qty_weak = 2
        super().__init__(energy_cost=2, card_type=CardType.ATTACK,
                         card_rarity=Rarity.COMMON, card_color=Color.RED,
                         *args, **kwargs)

    # TODO: make caller.take_damage a mangled method
    def use(self, caller, target, environment):
        caller.deal_damage(target, self.damage)
        target.increase_effect(Weak, self.qty_weak)

    def upgrade_logic(self):
        self.damage = 14
        self.qty_weak = 3


class Flex(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.strength_amount = 2
        super().__init__(energy_cost=0, card_type=CardType.SKILL,
                         card_rarity=Rarity.COMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller, target, environment):
        caller.increase_effect(Strength, self.strength_amount)
        caller.increase_effect(StrengthDownAtEndOfTurn, self.strength_amount)

    def upgrade_logic(self):
        self.strength_amount = 4


class Havoc(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(energy_cost=1, card_type=CardType.SKILL,
                         card_rarity=Rarity.COMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller, target, environment):
        did_we_draw_card = caller.draw_card(1)
        if did_we_draw_card:
            caller.use_card(target, caller.hand_pile[-1], environment['enemies'], is_free=True, will_discard=False)
            caller.exhaust_card(caller.hand_pile[-1])

    def upgrade_logic(self):
        self.energy_cost = 0


class Headbutt(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 9
        super().__init__(energy_cost=1, card_type=CardType.ATTACK,
                         card_rarity=Rarity.COMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller, target, environment):
        caller.deal_damage(target, self.damage)

        if caller.discard_pile:
            card = caller.select_card(caller.discard_pile, SelectEvent.PLACE_ON_DRAWPILE)
            caller.draw_pile.append(card)
            caller.discard_pile.remove(card)

    def upgrade_logic(self):
        self.damage = 12


class HeavyBlade(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.extra_strength_multiplier = 3
        super().__init__(energy_cost=2, card_type=CardType.ATTACK,
                         card_rarity=Rarity.COMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, 14 + (caller.get_effect_stacks(Strength) * (self.extra_strength_multiplier - 1)))

    def upgrade_logic(self):
        self.extra_strength_multiplier = 5


class IronWave(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 5
        self.block = 5
        super().__init__(energy_cost=1, card_type=CardType.ATTACK,
                         card_rarity=Rarity.COMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)
        caller.increase_effect(Block, self.block)

    def upgrade_logic(self):
        self.damage = 7
        self.block = 7


class PerfectedStrike(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.base_damage = 6
        self.increase = 2
        super().__init__(energy_cost=2, card_type=CardType.ATTACK,
                         card_rarity=Rarity.COMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        damage = self.base_damage
        for card in caller.get_combat_deck():
            if 'Strike' in card.name:
                damage += self.increase
        caller.deal_damage(target, damage)

    def upgrade_logic(self):
        self.increase = 3


class PommelStrike(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 9
        self.draw = 1
        super().__init__(energy_cost=1, card_type=CardType.ATTACK,
                         card_rarity=Rarity.COMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)
        caller.draw_card(self.draw)

    def upgrade_logic(self):
        self.damage = 10
        self.draw = 2


class ShrugItOff(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.block = 8
        super().__init__(energy_cost=1, card_type=CardType.SKILL,
                         card_rarity=Rarity.COMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(Block, self.block)
        caller.draw_card(1)

    def upgrade_logic(self):
        self.block = 11


class SwordBoomerang(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage_times = 3
        super().__init__(energy_cost=1, card_type=CardType.ATTACK,
                         card_rarity=Rarity.COMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        for _ in range(self.damage_times):
            caller.deal_damage(random.choice(environment['enemies']), 3)

    def upgrade_logic(self):
        self.damage_times = 4


class Thunderclap(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 4
        super().__init__(energy_cost=1, card_type=CardType.ATTACK,
                         card_rarity=Rarity.COMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        for enemy in environment['enemies']:
            caller.deal_damage(enemy, self.damage)
            caller.increase_effect(Vulnerable, 1)

    def upgrade_logic(self):
        self.damage = 7


class TrueGrit(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.block = 7
        super().__init__(energy_cost=1, card_type=CardType.SKILL,
                         card_rarity=Rarity.COMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(Block, self.block)
        if len(caller.hand_pile) > 1:
            if self.upgraded:
                caller.exhaust_card(caller.select_card(caller.get_hand_without(self), SelectEvent.EXHAUST))
            else:
                caller.exhaust_card(random.choice(caller.get_hand_without(self)))

    def upgrade_logic(self):
        self.block = 9


class TwinStrike(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 5
        super().__init__(energy_cost=1, card_type=CardType.ATTACK,
                         card_rarity=Rarity.COMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        pass

        for _ in range(2):
            caller.deal_damage(target, self.damage)

    def upgrade_logic(self):
        self.damage = 7


class Warcry(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.draw_num = 1
        super().__init__(energy_cost=0, card_type=CardType.SKILL, exhaust=True,
                         card_rarity=Rarity.COMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.draw_card(self.draw_num)
        caller.draw_pile.append(caller.select_card(caller.get_hand_without(self), SelectEvent.PLACE_ON_DRAWPILE))

    def upgrade_logic(self):
        self.draw_num = 2


class WildStrike(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 12
        super().__init__(energy_cost=1, card_type=CardType.ATTACK,
                         card_rarity=Rarity.COMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)
        caller.add_card_to_draw(Wound(), shuffle=True)

    def upgrade_logic(self):
        self.damage = 17


class BattleTrance(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.draw_qty = 3
        super().__init__(energy_cost=0, card_type=CardType.SKILL,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.draw_card(self.draw_qty)
        caller.set_effect(NoDraw, 1)

    def upgrade_logic(self):
        self.draw_qty = 4


class BloodForBlood(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 18
        super().__init__(energy_cost=4, card_type=CardType.ATTACK,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)

    def upgrade_logic(self):
        self.energy_cost = 3
        self.damage = 22

    def cost(self, actor):
        return self.energy_cost - actor.times_received_damage


class Bloodletting(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.energy_gain = 2
        super().__init__(energy_cost=0, card_type=CardType.SKILL,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.receive_damage_from_card(3, self)
        caller.gain_energy(self.energy_gain)

    def upgrade_logic(self):
        self.energy_gain = 3


class BurningPact(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.card_draw = 2
        super().__init__(energy_cost=1, card_type=CardType.SKILL,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.draw_card(self.card_draw)
        caller.exhaust_card(caller.select_card(caller.get_hand_without(self), SelectEvent.EXHAUST))

    def upgrade_logic(self):
        self.card_draw = 3


class Carnage(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 20
        super().__init__(energy_cost=2, card_type=CardType.ATTACK, ethereal=True,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)

    def upgrade_logic(self):
        self.damage = 28


class Combust(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.stacks = 5
        super().__init__(energy_cost=1, card_type=CardType.POWER,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(effects.CombustEffect, self.stacks)

    def upgrade_logic(self):
        self.stacks = 7


class DarkEmbrace(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(energy_cost=2, card_type=CardType.POWER,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(DarkEmbraceEffect, 1)

    def upgrade_logic(self):
        self.energy_cost = 1


class Disarm(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.strength_loss = 2
        super().__init__(energy_cost=1, card_type=CardType.SKILL, exhaust=True,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        target.decrease_effect(Strength, self.strength_loss)

    def upgrade_logic(self):
        self.strength_loss = 3


class Dropkick(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 5
        super().__init__(energy_cost=1, card_type=CardType.ATTACK,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)
        if target.has_effect(Vulnerable):
            caller.gain_energy()
            caller.draw_card()

    def upgrade_logic(self):
        self.damage = 8


class DuelWield(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(energy_cost=1, card_type=CardType.SKILL,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        # Have the actor select a valid card
        card = caller.select_card(
            event_type=SelectEvent.COPY,
            options=caller.get_cards(
                from_piles=[CardPiles.HAND],
                with_types=[CardType.ATTACK, CardType.POWER]))

        # Add one to hand
        caller.add_card_to_hand(deepcopy(card))

        # And if upgraded add a second
        if self.upgraded:
            caller.add_card_to_hand(deepcopy(card))

    def upgrade_logic(self):
        pass


class Entrench(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(energy_cost=2, card_type=CardType.SKILL,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(Block, caller.get_effect_stacks(Block))

    def upgrade_logic(self):
        self.energy_cost = 1


class Evolve(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.draw = 1
        super().__init__(energy_cost=1, card_type=CardType.POWER,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(EvolveEffect, self.draw)

    def upgrade_logic(self):
        self.draw = 2


class FeelNoPain(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.block = 3
        super().__init__(energy_cost=1, card_type=CardType.POWER,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(FeelNoPainEffect, self.block)

    def upgrade_logic(self):
        self.block = 4


class FireBreathing(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 6
        super().__init__(energy_cost=1, card_type=CardType.POWER,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(FireBreathingEffect, self.damage)

    def upgrade_logic(self):
        self.damage = 10


class FlameBarrier(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 4
        super().__init__(energy_cost=2, card_type=CardType.SKILL,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(FlameBarrierEffect, self.damage)

    def upgrade_logic(self):
        self.damage = 6


class GhostlyArmor(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.block = 10
        super().__init__(energy_cost=1, card_type=CardType.SKILL, ethereal=True,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(Block, self.block)

    def upgrade_logic(self):
        self.block = 13


class Hemokinesis(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 15
        super().__init__(energy_cost=1, card_type=CardType.ATTACK,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)
        caller.receive_damage_from_card(2, self)

    def upgrade_logic(self):
        self.damage = 20


class InfernalBlade(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(energy_cost=1, card_type=CardType.SKILL, exhaust=True,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

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
    def __init__(self, *args, **kwargs):
        self.str = 2
        super().__init__(energy_cost=1, card_type=CardType.POWER,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(Strength, self.str)

    def upgrade_logic(self):
        self.str = 3


class Intimidate(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.weak = 1
        super().__init__(energy_cost=0, card_type=CardType.SKILL, exhaust=True,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        for enemy in environment['enemies']:
            enemy: AbstractEnemy
            enemy.increase_effect(Weak, self.weak)

    def upgrade_logic(self):
        self.weak = 2


class Metallicize(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.metal = 3
        super().__init__(energy_cost=1, card_type=CardType.POWER,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(MetallicizeEffect, self.metal)

    def upgrade_logic(self):
        self.metal = 4


class PowerThrough(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.block_qty = 15
        super().__init__(energy_cost=1, card_type=CardType.SKILL,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.add_card_to_hand(Wound)
        caller.add_card_to_hand(Wound)
        caller.increase_effect(Block, self.block_qty)

    def upgrade_logic(self):
        self.block_qty = 20


class Pummel(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.times = 4
        super().__init__(energy_cost=1, card_type=CardType.ATTACK, exhaust=True,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        for i in range(self.times):
            caller.deal_damage(target, 4)

    def upgrade_logic(self):
        self.times = 5


class Rage(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.stack_qty = 3
        super().__init__(energy_cost=0, card_type=CardType.SKILL,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(RageEffect, self.stack_qty)

    def upgrade_logic(self):
        self.stack_qty = 5


class Rampage(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 8
        self.upgrade_amount = 5
        super().__init__(energy_cost=1, card_type=CardType.ATTACK,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)
        self.damage += self.upgrade_amount

    def upgrade_logic(self):
        self.upgrade_amount = 8


class RecklessCharge(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 7
        super().__init__(energy_cost=0, card_type=CardType.ATTACK,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)
        caller.add_card_to_draw(Dazed, shuffle=True)

    def upgrade_logic(self):
        self.damage = 10


class Rupture(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.strength = 1
        super().__init__(energy_cost=1, card_type=CardType.POWER,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(RuptureEffect, self.strength)

    def upgrade_logic(self):
        self.strength = 2


class SearingBlow(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.upgraded_qty = 0
        super().__init__(energy_cost=2, card_type=CardType.ATTACK, allow_multiple_upgrades=True,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, 12 + (4 * self.upgraded_qty))

    def upgrade_logic(self):
        self.upgraded_qty += 1


class SecondWind(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.block_per_card = 5
        super().__init__(energy_cost=1, card_type=CardType.SKILL,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        # After
        for card in caller.get_cards(
                from_piles=CardPiles.HAND,
                with_types=CardType.ATTACK,
                exclude_cards=self):
            caller.exhaust_card(card)
            caller.increase_effect(Block, self.block_per_card)

    def upgrade_logic(self):
        self.block_per_card = 7


class SeeingRed(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(energy_cost=1, card_type=CardType.SKILL, exhaust=True,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.gain_energy(2)

    def upgrade_logic(self):
        self.energy_cost = 0


class Sentinel(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.block = 5
        self.energy_to_gain = 2
        super().__init__(energy_cost=1, card_type=CardType.SKILL,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(Block, self.block)

    def on_exhaust(self, caller):
        caller.gain_energy(self.energy_to_gain)

    def upgrade_logic(self):
        self.block = 8
        self.energy_to_gain = 3


class SeverSoul(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 16
        super().__init__(energy_cost=2, card_type=CardType.ATTACK,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        for card in caller.get_cards(
                from_piles=CardPiles.HAND,
                exclude_cards=[self]):
            caller.exhaust_card(card)

        caller.deal_damage(target, self.damage)

    def upgrade_logic(self):
        self.damage = 22


class Shockwave(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.effect_amount = 3
        super().__init__(energy_cost=2, card_type=CardType.SKILL, exhaust=True,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        for enemy, effect in product(environment['enemies'], (Weak, Vulnerable)):
            enemy.increase_effect(effect, self.effect_amount)

    def upgrade_logic(self):
        self.effect_amount = 5


class SpotWeakness(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.strength_amount = 3
        super().__init__(energy_cost=1, card_type=CardType.SKILL,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        if target.intent in (IntentType.AGGRESSIVE, IntentType.AGGRESSIVE_DEBUFF,
                             IntentType.AGGRESSIVE_BUFF, IntentType.AGGRESSIVE_DEFENSE):
            caller.increase_effect(Strength, self.strength_amount)

    def upgrade_logic(self):
        self.strength_amount = 4


class Uppercut(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.effect_amount = 1
        super().__init__(energy_cost=2, card_type=CardType.ATTACK,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, 13)
        for effect in (Weak, Vulnerable):
            target.increase_effect(effect, self.effect_amount)

    def upgrade_logic(self):
        self.effect_amount = 2


class Whirlwind(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 5
        super().__init__(energy_cost='X', card_type=CardType.ATTACK,
                         card_rarity=Rarity.UNCOMMON, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        for enemy in environment['enemies']:
            for _ in range(self.energy_cost):
                caller.deal_damage(enemy, self.damage)

    def upgrade_logic(self):
        self.damage = 8


# TODO: Effect is bugged?
class Barricade(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(energy_cost=3, card_type=CardType.POWER,
                         card_rarity=Rarity.RARE, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(BarricadeEffect, 1)

    def upgrade_logic(self):
        self.energy_cost = 2


# TODO: Effect
class Berserk(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.vulnerable = 2
        super().__init__(energy_cost=0, card_type=CardType.POWER,
                         card_rarity=Rarity.RARE, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(BerserkEffect, 1)
        caller.increase_effect(Vulnerable, self.vulnerable)

    def upgrade_logic(self):
        self.vulnerable = 1


class Bludgeon(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 32
        super().__init__(energy_cost=3, card_type=CardType.ATTACK,
                         card_rarity=Rarity.RARE, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)

    def upgrade_logic(self):
        self.damage = 42


# TODO: Effect
class Brutality(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(energy_cost=0, card_type=CardType.POWER,
                         card_rarity=Rarity.RARE, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(BrutalityEffect, 1)

    def upgrade_logic(self):
        self.innate = True


# TODO: Effect
class Corruption(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(energy_cost=3, card_type=CardType.POWER,
                         card_rarity=Rarity.RARE, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(CorruptionEffect, 1)

    def upgrade_logic(self):
        self.energy_cost = 2


# TODO: Effect
class DemonForm(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.demon_form_stacks = 2
        super().__init__(energy_cost=3, card_type=CardType.POWER,
                         card_rarity=Rarity.RARE, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(DemonFormEffect, self.demon_form_stacks)

    def upgrade_logic(self):
        self.demon_form_stacks = 3


# TODO: Effect
class DoubleTap(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.double_tap_stacks = 1
        super().__init__(energy_cost=1, card_type=CardType.SKILL,
                         card_rarity=Rarity.RARE, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(DoubleTapEffect, self.double_tap_stacks)

    def upgrade_logic(self):
        self.double_tap_stacks = 2


# TODO: Test
class Exhume(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(energy_cost=1, card_type=CardType.SKILL, exhaust=True,
                         card_rarity=Rarity.RARE, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        card = caller.select_card(
            caller.get_cards(
                from_piles=CardPiles.EXHAUST,
                exclude_cards=self),
            event_type=SelectEvent.RECOVER_FROM_EXHAUST)
        caller.recover_card(card)

    def upgrade_logic(self):
        self.energy_cost = 0


# TODO: Test
class Feed(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 10
        self.gain = 3
        super().__init__(energy_cost=1, card_type=CardType.ATTACK,
                         card_rarity=Rarity.RARE, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.deal_damage(target, self.damage)

    def upgrade_logic(self):
        self.damage = 12
        self.gain = 4

    def on_fatal(self, caller):
        caller.max_health += self.gain


# TODO: Test
class FiendFire(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 7
        super().__init__(energy_cost=2, card_type=CardType.ATTACK,
                         card_rarity=Rarity.RARE, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        # I don't know for sure, but my impression is that
        # all the cards are exhausted and THEN all the damage is dealt
        # so that's how I'm implementing it here
        qty = 0
        for card in caller.get_cards(
                from_piles=CardPiles.HAND,
                exclude_cards=self):
            caller.exhaust_card(card)
            qty += 1

        for _ in range(qty):
            caller.deal_damage(target, self.damage)

    def upgrade_logic(self):
        self.damage = 10


# TODO: Implement Burn
class Immolate(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.damage = 21
        super().__init__(energy_cost=2, card_type=CardType.ATTACK,
                         card_rarity=Rarity.RARE, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        for enemy in environment['enemies']:
            caller.deal_damage(enemy, self.damage)
            caller.add_card_to_exhaust(Burn())

    def upgrade_logic(self):
        self.damage = 28


# TODO: Test
class Impervious(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.quantity = 30
        super().__init__(energy_cost=2, card_type=CardType.SKILL,
                         card_rarity=Rarity.RARE, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(Block, self.quantity)

    def upgrade_logic(self):
        self.quantity = 40


class Juggernaut(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        self.stacks = 5
        super().__init__(energy_cost=2, card_type=CardType.POWER,
                         card_rarity=Rarity.RARE, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(JuggernautEffect, self.stacks)

    def upgrade_logic(self):
        self.stacks = 7


# TODO: Test
class LimitBreak(AbstractCard, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(energy_cost=1, card_type=CardType.SKILL, exhaust=True,
                         card_rarity=Rarity.RARE, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.increase_effect(Strength, caller.get_effect_stacks(Strength))

    def upgrade_logic(self):
        self.exhaust = False


# TODO: Test
class Offering(AbstractCard, ABC):
    """Lose 6 HP. Gain 2 energy. Draw 3(5) cards. Exhaust."""

    def __init__(self, *args, **kwargs):
        self.cards = 3
        super().__init__(energy_cost=0, card_type=CardType.SKILL, exhaust=True,
                         card_rarity=Rarity.RARE, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        caller.receive_damage_from_card(6, self)
        caller.gain_energy(2)
        caller.draw_card(self.cards)

    def upgrade_logic(self):
        self.cards = 5


# TODO: TEST
# This was designed using deal_damage, which may need to be refactored if it doesn't return damage dealt
class Reaper(AbstractCard, ABC):
    """	Deal 4(5) damage to ALL enemies. Heal HP equal to unblocked damage. Exhaust."""

    def __init__(self, *args, **kwargs):
        self.damage = 4
        super().__init__(energy_cost=2, card_type=CardType.ATTACK,
                         card_rarity=Rarity.RARE, card_color=Color.RED,
                         *args, **kwargs)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        damage = 0
        for enemy in environment['enemies']:
            damage += caller.deal_damage(enemy, self.damage)
        caller.heal(damage)

    def upgrade_logic(self):
        self.damage = 5


card_classes = {
    (card_cls.sts_name if hasattr(card_cls, 'sts_name') else card_cls.__name__): card_cls
    for card_cls in AbstractCard.__subclasses__()
}