import random
from abc import ABC, abstractmethod

from typing import TYPE_CHECKING
from enum import Enum
from new.effects import *
from new.actors import SelectEvent
if TYPE_CHECKING:
    from actors import AbstractActor
    from enemies import AbstractEnemy


class CardType(Enum):
    ATTACK = 1
    SKILL = 2
    POWER = 3
    STATUS = 4
    CURSE = 5


class AbstractCard(ABC):
    """
    Abstract card class is the blueprint for all cards. The goal for this class
    is to allow simple, quick implementation of Slay the Spire cards. To use write an implementation
    for a card, write a class that inherits this class as well as ABC, then implement an __init__,
    use, and upgrade_logic methods.
    """

    def __init__(self, energy_cost: int, card_type: CardType, upgraded: bool = False, name: str = None):
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

        # If the card is upgraded or not
        self.upgraded: bool = upgraded

        # Type of card
        self.card_type: CardType = card_type

    @abstractmethod
    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', all_enemies):
        """Overriding this method provides the default behavior of a card."""
        pass

    def upgrade(self):
        if self.upgraded:
            return

        self.name = self.name + "+"
        self.upgraded = True
        self.upgrade_logic()

    @abstractmethod
    def upgrade_logic(self):
        """Overriding this method provides the behavior of the card on upgrade."""
        pass

    def is_playable(self, caller):
        return True

    # Override the str() method so printing it returns the name
    def __str__(self):
        return self.name

    # Override the repr() method so arrays print neatly
    def __repr__(self):
        return self.name


class RedStrike(AbstractCard, ABC):
    def __init__(self):
        self.damage = 6
        super().__init__(name='Strike', energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        caller.deal_damage(target, self.damage)

    def upgrade_logic(self):
        self.damage = 9


class RedDefend(AbstractCard, ABC):
    def __init__(self):
        self.block = 5
        super().__init__(name='Defend', energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        caller.increase_effect(Block, self.block)

    def upgrade_logic(self):
        self.block = 8


class Bash(AbstractCard, ABC):
    def __init__(self):
        self.damage = 8
        self.vulnerable = 2
        super().__init__(energy_cost=2, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        caller.deal_damage(target, self.damage)
        target.increase_effect(Vulnerable, self.vulnerable)

    def upgrade_logic(self):
        self.damage = 10
        self.vulnerable = 3


class Anger(AbstractCard, ABC):
    def __init__(self):
        self.damage = 6
        super().__init__(energy_cost=0, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        caller.deal_damage(target, self.damage)
        caller.discard_pile.append(Anger())

    def upgrade_logic(self):
        self.damage = 8


class Armaments(AbstractCard, ABC):
    def __init__(self):
        self.block = 5
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller, target, enemies):
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

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        if caller.effects.get(Block):
            caller.deal_damage(target, caller.get_effect_stacks(Block))

    def upgrade_logic(self):
        self.energy_cost = 0


class Clash(AbstractCard, ABC):

    def __init__(self):
        self.damage = 14
        super().__init__(energy_cost=0, card_type=CardType.ATTACK)

    def use(self, caller, target, enemies):
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

    def use(self, caller, target, enemies):
        for enemy in enemies:
            caller.deal_damage(enemy, self.damage)

    def upgrade_logic(self):
        self.damage = 11


class Clothesline(AbstractCard, ABC):
    def __init__(self):
        self.damage = 12
        self.qty_weak = 2
        super().__init__(energy_cost=2, card_type=CardType.ATTACK)

    # TODO: make caller.take_damage a mangled method
    def use(self, caller, target, enemies):
        caller.deal_damage(target, self.damage)
        target.increase_effect(Weak, self.qty_weak)

    def upgrade_logic(self):
        self.damage = 14
        self.qty_weak = 3


class Flex(AbstractCard, ABC):
    def __init__(self):
        self.strength_amount = 2
        super().__init__(energy_cost=0, card_type=CardType.SKILL)

    def use(self, caller, target, enemies):
        caller.increase_effect(Strength, self.strength_amount)
        caller.increase_effect(StrengthDown, self.strength_amount)

    def upgrade_logic(self):
        self.strength_amount = 4


class Havoc(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller, target, enemies):
        did_we_draw_card = caller.draw_card(1)
        if did_we_draw_card:
            caller.use_card(target, caller.hand_pile[-1], enemies, is_free=True, will_discard=False)
            caller.exhaust_card(caller.hand_pile[-1])

    def upgrade_logic(self):
        self.energy_cost = 0


class Headbutt(AbstractCard, ABC):
    def __init__(self):
        self.damage = 9
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller, target, enemies):
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

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', all_enemies):
        caller.deal_damage(target, 14 + (caller.get_effect_stacks(Strength) * (self.extra_strength_multiplier - 1)))

    def upgrade_logic(self):
        self.extra_strength_multiplier = 5


class IronWave(AbstractCard, ABC):
    def __init__(self):
        self.damage = 5
        self.block = 5
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', all_enemies):
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

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', all_enemies):
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

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', all_enemies):
        caller.deal_damage(target, self.damage)
        caller.draw_card(self.draw)

    def upgrade_logic(self):
        self.damage = 10
        self.draw = 2


class ShrugItOff(AbstractCard, ABC):
    def __init__(self):
        self.block = 8
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', all_enemies):
        caller.increase_effect(Block, self.block)
        caller.draw_card(1)

    def upgrade_logic(self):
        self.block = 11


class SwordBoomerang(AbstractCard, ABC):
    def __init__(self):
        self.damage_times = 3
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', all_enemies):
        for _ in range(self.damage_times):
            caller.deal_damage(random.choice(all_enemies), 3)

    def upgrade_logic(self):
        self.damage_times = 4


##########################
######################TODO
##########################

class Thunderclap(AbstractCard, ABC):
    def __init__(self):
        self.damage = 4
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        for enemy in enemies:
            caller.deal_damage(enemy, self.damage)
            caller.increase_effect(Vulnerable, 1)


    def upgrade_logic(self):
        self.damage = 7


class TrueGrit(AbstractCard, ABC):
    def __init__(self):
        self.block = 7
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        caller.increase_effect(Block, self.block)
        if self.upgraded:
            caller.exhaust_card(caller.select_card(caller.hand_pile, SelectEvent.EXHAUST))
        else:
            caller.exhaust_card(random.choice(caller.hand_pile))


    def upgrade_logic(self):
        self.block = 9
    
    
class TwinStrike(AbstractCard, ABC):
    def __init__(self):
        self.damage = 5
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

        for _ in range(2):
            caller.deal_damage(target, self.damage)

    def upgrade_logic(self):
        self.damage = 7
    
    
class Warcry(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=0, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class WildStrike(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class BattleTrance(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=0, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class BloodForBlood(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=4, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Bloodletting(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=0, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class BurningPact(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Carnage(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=2, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Combust(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class DarkEmbrace(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=2, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Disarm(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Dropkick(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class DuelWield(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Entrench(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=2, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Evolve(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class FeelNoPain(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Firebreathing(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class FlameBarrier(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=2, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class GhostlyArmor(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Hemokinesis(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class InfernalBlade(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Inflame(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Intimidate(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=0, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Metallicize(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class PowerThrough(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Pummel(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Rage(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=0, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Rampage(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class RecklessCharge(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=0, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Rupture(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class SearingBlow(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=2, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class SecondWind(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class SeeingRed(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Sentinel(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class SeverSoul(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=2, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Shockwave(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=2, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class SpotWeakness(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Uppercut(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=2, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Whirlwind(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost='x', card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Barricade(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=3, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Berserk(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=0, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Bludgeon(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=3, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Brutality(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=0, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Corruption(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=3, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class DemonForm(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=3, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class DoubleTap(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Exhume(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Feed(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class FiendFire(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=2, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Immolate(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=2, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Impervious(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=2, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Juggernaut(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=2, card_type=CardType.POWER)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class LimitBreak(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=1, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Offering(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=0, card_type=CardType.SKILL)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass


class Reaper(AbstractCard, ABC):
    def __init__(self):
        super().__init__(energy_cost=2, card_type=CardType.ATTACK)

    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', enemies):
        pass

    def upgrade_logic(self):
        pass
