from abstractions import *
from enumerations import *
from effects import *


class BurningBlood(AbstractRelic):
    """Gain 6 health at the end of combat."""
    def __init__(self):
        super().__init__(relic_color=Color.RED,
                         relic_rarity=Rarity.STARTER)

    def on_end_combat(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment):
        owner.heal(6)


class RingOfTheSnake(AbstractRelic):
    """At the start of combat draw 2 additional cards"""

    def __init__(self):
        super(RingOfTheSnake, self).__init__(relic_rarity=Rarity.STARTER,
                                             relic_color=Color.GREEN)

    def on_enter_combat(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment):
        owner.draw_card(quantity=2)


class CrackedCore(AbstractRelic):
    pass


class PureWater(AbstractRelic):
    pass


class Akabeko(AbstractRelic):
    """at the start of combat gain 8 vigor,
     common uncolored"""
    def __init__(self):
        super().__init__(relic_color=Color.COLORLESS,
                         relic_rarity=Rarity.COMMON)

    def on_enter_combat(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment):
        owner.increase_effect(Vigor, 8)


class Anchor(AbstractRelic):
    """at the start of combat gain 10 block,
     common uncolored"""

    def __init__(self):
        super(Anchor, self).__init__(relic_rarity=Rarity.COMMON,
                                     relic_color=Color.COLORLESS)

    def on_enter_combat(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment):
        owner.increase_effect(effect=Block, value=10)


class AncientTeaSet(AbstractRelic):
    """enter rest site, next combat start with 2 additional energy,
     common uncolored"""
    def __init__(self):
        self.DrankTea = False
        super().__init__(relic_rarity=Rarity.COMMON,
                         relic_color=Color.COLORLESS)

    def on_enter_rest_site(self, owner: AbstractActor | AbstractEnemy, environment):
        self.DrankTea = True

    def on_enter_combat(self, owner: AbstractActor | AbstractEnemy, environment):
        if self.DrankTea:  # bless tea time.
            owner.increase_effect(Energy, 2)
            self.DrankTea = False  # tea is gone, quite sad.


class ArtOfWar(AbstractRelic):
    """at the end of turn, if you have not played an attack, next turn gain 1 extra energy,
    common uncolored"""
    def __init__(self):
        self.noAttacks = True
        self.doGiveEnergy = False
        super().__init__(relic_rarity=Rarity.COMMON,
                         relic_color=Color.COLORLESS)

    def on_card_play(self, owner: AbstractActor | AbstractEnemy, environment, card: AbstractCard):
        if card.card_type == CardType.ATTACK:
            self.noAttacks = False

    def on_end_turn(self, owner: AbstractActor | AbstractEnemy, environment):
        if self.noAttacks:
            self.doGiveEnergy = True
        else:
            self.doGiveEnergy = False

    def on_start_turn(self, owner: AbstractActor | AbstractEnemy, environment):
        self.noAttacks = True

        if self.doGiveEnergy:
            owner.increase_effect(Energy, 1)


class BagOfMarbles(AbstractRelic):
    """at the start of combat, apply 1 vulnerable to all enemies,
    common uncolored"""
    def __init__(self):
        super(BagOfMarbles, self).__init__(relic_rarity=Rarity.COMMON,
                                           relic_color=Color.COLORLESS)

    def on_enter_combat(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment):
        for enemy in environment.enemies:
            enemy.increaseEffect(Vulnerable, 1)


class BagOfPreparation(AbstractRelic):
    """at the start of combat draw 2 additional cards,
    common uncolored"""

    def __init__(self):
        super(BagOfPreparation, self).__init__(relic_rarity=Rarity.COMMON,
                                               relic_color=Color.COLORLESS)

    def on_enter_combat(self, owner: AbstractActor | AbstractEnemy, environment: AbstractCombat):
        owner.draw_card(2)


class BloodVial(AbstractRelic):
    """at the start of combat heal 2 hp,
    common uncolored"""

    def __init__(self):
        super(BloodVial, self).__init__(relic_rarity=Rarity.COMMON,
                                        relic_color=Color.COLORLESS)

    def on_enter_combat(self, owner: AbstractActor | AbstractEnemy, environment: AbstractCombat):
        owner.heal(2)


class BronzeScales(AbstractRelic):
    """at the start of combat gain 3 thorns,
    common uncolored"""

    def __init__(self):
        super(BronzeScales, self).__init__(relic_rarity=Rarity.COMMON,
                                           relic_color=Color.COLORLESS)

    def on_enter_combat(self, owner: AbstractActor | AbstractEnemy, environment: AbstractCombat):
        owner.increase_effect(Thorns, 3)


class CentennialPuzzle(AbstractRelic):
    """the first time you lose hp this combat, draw 3 cards,
    common uncolored"""

    def __init__(self):
        super(CentennialPuzzle, self).__init__(relic_rarity=Rarity.COMMON,
                                               relic_color=Color.COLORLESS)

        self.notLostHealth = True

    def on_enter_combat(self, owner: AbstractActor | AbstractEnemy, environment: AbstractCombat):
        self.notLostHealth = True

    def on_lose_hp(self, owner: AbstractActor | AbstractEnemy, environment):
        owner.draw_card(3)
        self.notLostHealth = False


class CeramicFish(AbstractRelic):
    """when you add a card to your deck, gain 9 gold,
    common uncolored"""

    def __init__(self):
        super(CeramicFish, self).__init__(relic_rarity=Rarity.COMMON,
                                          relic_color=Color.COLORLESS)

    def on_add_card_to_deck(self, owner:AbstractActor | AbstractEnemy, environment, card):
        owner.gold += 9


class DreamCatcher(AbstractRelic):
    """when you rest, you may add a card to your deck,
    common uncolored"""

    def __init__(self):
        super(DreamCatcher, self).__init__(relic_rarity=Rarity.COMMON,
                                           relic_color=Color.COLORLESS)

    def on_rest(self, owner: AbstractActor, environment):
        environment.promptCardReward()


class HappyFlower(AbstractRelic):
    """every 3 turns gain 1 energy
    common uncolored"""

    def __init__(self):
        super(HappyFlower, self).__init__(relic_rarity=Rarity.COMMON,
                                          relic_color=Color.COLORLESS)
        self.numberOfTurns = 0

    def on_start_turn(self, owner: AbstractActor | AbstractEnemy, environment):
        if self.numberOfTurns >= 3:
            self.numberOfTurns = 0
            owner.increase_effect(Energy, 1)
        else:
            self.numberOfTurns += 1


class JuzuBracelet(AbstractRelic):
    """regular enemy combats are no longer encountered in ? rooms,
    common uncolored"""


class Lantern(AbstractRelic):
    """gain 1 energy, at the start of each combat,
    common uncolored"""

    def __init__(self):
        super(Lantern, self).__init__(relic_rarity=Rarity.COMMON,
                                      relic_color=Color.COLORLESS)

    def on_enter_combat(self, owner: AbstractActor | AbstractEnemy, environment: AbstractCombat):
        owner.increase_effect(Energy, 1)


class MawBank(AbstractRelic):
    """when you climb a floor gain 12 gold, unless you shopped since getting this.
    common uncolored"""

    def __init__(self):
        super(MawBank, self).__init__(relic_rarity=Rarity.COMMON,
                                      relic_color=Color.COLORLESS)
        self.goldEveryFloor = True

    def on_floor_climb(self, owner: AbstractActor | AbstractEnemy, environment):
        if self.goldEveryFloor:
            owner.gain_gold(12)

    def on_gold_spent_shopping(self, owner: AbstractActor, environment, card):
        self.goldEveryFloor = False


class MealTicket(AbstractRelic):
    """whenever you enter a shop heal 15 hp
    common uncolored"""

    def __init__(self):
        super(MealTicket, self).__init__(relic_rarity=Rarity.COMMON,
                                         relic_color=Color.COLORLESS)

    def on_enter_shop(self, owner: AbstractActor | AbstractEnemy, environment):
        owner.heal(15)


class Nunchaku(AbstractRelic):
    """every time you play 10 attacks gain 1 energy,
    common uncolored"""

    def __init__(self):
        super(Nunchaku, self).__init__(relic_rarity=Rarity.COMMON,
                                       relic_color=Color.COLORLESS)

        self.countAttacks = 0

    def on_card_play(self, owner: AbstractActor | AbstractEnemy, environment, card):
        if card.card_type == CardType.ATTACK:
            self.countAttacks += 1

            if self.countAttacks >= 10:
                owner.increase_effect(Energy, 1)
                self.countAttacks = 0


class OddlySmoothStone(AbstractRelic):
    """at the start of combat gain 1 dexterity,
    common uncolored"""

    def __init__(self):
        super(OddlySmoothStone, self).__init__(relic_rarity=Rarity.COMMON,
                                               relic_color=Color.COLORLESS)

    def on_enter_combat(self, owner: AbstractActor | AbstractEnemy, environment: AbstractCombat):
        owner.increase_effect(Dexterity, 1)


class Omamori(AbstractRelic):
    """negate the next 2 curses you obtain
    common uncolored"""

    def __init__(self):
        super(Omamori, self).__init__(relic_rarity=Rarity.COMMON,
                                      relic_color=Color.COLORLESS)

        self.negateThisCountCurses = 2

    def on_add_curse_to_deck(self, owner: AbstractActor, environment, curse):

        if self.negateThisCountCurses > 0:
            self.negateThisCountCurses -= 1
        else:
            owner.add_card_to_hand(curse)


class Orichalcum(AbstractRelic):
    """if you end your turn without block, gain 6 block,
    common uncolored"""

    def __init__(self):
        super(Orichalcum, self).__init__(relic_rarity=Rarity.COMMON,
                                         relic_color=Color.COLORLESS)

    def on_end_turn(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment):
        if owner.has_effect(Block, 0):
            owner.increase_effect(Block, 6)


class PenNib(AbstractRelic):
    """every 10th attack you play deals double damage,
    common uncolored"""
    def __init__(self):
        super(PenNib, self).__init__(relic_rarity=Rarity.COMMON,
                                     relic_color=Color.COLORLESS)
        self.numberOfAttacks = 0

    def on_card_play(self, owner: AbstractActor | AbstractEnemy, environment, card):
        if card.card_type == CardType.ATTACK:
            self.numberOfAttacks += 1
            if self.numberOfAttacks >= 9:
                owner.increase_effect(DoubleDamageForOneAttack, 1)
                self.numberOfAttacks = 0


class PotionBelt(AbstractRelic):
    """upon pickup gain 2 potion slots,
    common uncolored"""

    def __init__(self):
        super(PotionBelt, self).__init__(relic_rarity=Rarity.COMMON,
                                         relic_color=Color.COLORLESS)

    def on_pickup_relic(self, owner: AbstractActor, environment, card):
        owner.potionSlotsOpen += 2


class PreservedInsect(AbstractRelic):
    """enemies in elite rooms now have 25% less health,
    common uncolored"""


class RegalPillow(AbstractRelic):
    """heal an additional 15 hp when you rest,
    common uncolored"""


class SmilingMask(AbstractRelic):
    """merchant card removal now always costs 50 gold,
    common uncolored"""


class Strawberry(AbstractRelic):
    """upon pickup raise max hp by 7,
    common uncolored"""


class TheBoot(AbstractRelic):
    """whenever you would deal 4 or less unblocked damage, deal 5,
    common uncolored"""


class TinyChest(AbstractRelic):
    """every 4th ? is a treasure room,
    common uncolored"""


class ToyOrnithopter(AbstractRelic):
    """whenever you use a potion heal 5 hp,
    common uncolored"""


class Vajra(AbstractRelic):
    """at the start of combat gain 1 strength,
    common uncolored"""


class WarPaint(AbstractRelic):
    """upon pickup upgrade 2 random skills,
    common uncolored"""


class Whetstone(AbstractRelic):
    """upon pickup upgrade 2 random attacks,
    common uncolored"""
