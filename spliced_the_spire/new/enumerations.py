from enum import Enum


class SelectEvent(Enum):
    DRAW = 1
    EXHAUST = 2
    PLACE_ON_DRAWPILE = 3
    COPY = 4
    RECOVER_FROM_EXHAUST = 5
    DISCARD = 6


class CardPiles(Enum):
    DRAW = 1
    HAND = 2
    DISCARD = 3
    EXHAUST = 4

    @classmethod
    def all(cls):
        return CardPiles.DRAW, CardPiles.HAND, CardPiles.DISCARD, CardPiles.EXHAUST


class CardType(Enum):
    UNKNOWN = 0
    ATTACK = 1
    SKILL = 2
    POWER = 3
    STATUS = 4
    CURSE = 5

    @staticmethod
    def all():
        return CardType.ATTACK, CardType.SKILL, CardType.POWER, CardType.STATUS, CardType.CURSE


class Rarity(Enum):
    UNKNOWN = 0
    STARTER = 1
    COMMON = 2
    UNCOMMON = 3
    RARE = 4
    SPECIAL = 5


class Color(Enum):
    UNKNOWN = 0
    COLORLESS = 1
    RED = 2
    GREEN = 3
    BLUE = 4
    PURPLE = 5


class IntentIcon(Enum):
    DAGGER = 1
    KNIFE = 2
    SWORD = 3
    SCIMITAR = 4
    BUTCHER = 5
    AXE = 6
    SCYTHE = 7
    SHIELD = 8
    SMALL_DEBUFF = 9
    BIG_DEBUFF = 10
    BUFF = 11
    DAGGER_DEBUFF = 12
    SWORD_DEBUFF = 13
    SCIMITAR_DEBUFF = 14
    BUTCHER_DEBUFF = 15
    AXE_DEBUFF = 16
    DAGGER_BLOCK = 17
    SWORD_BLOCK = 18
    SCIMITAR_BLOCK = 19
    SCYTHE_BLOCK = 20
    SWORD_BUFF = 21
    BLOCK_BUFF = 22
    BLOCK_DEBUFF = 23
    COWARDLY = 24
    SLEEPING = 25
    STUNNED = 26
    UNKNOWN = 27


class IntentType(Enum):
    AGGRESSIVE = 1
    DEFENSIVE = 2
    DEBUFF = 3
    BUFF = 4
    AGGRESSIVE_DEBUFF = 5
    AGGRESSIVE_DEFENSE = 6
    AGGRESSIVE_BUFF = 7
    DEFENSIVE_BUFF = 8
    DEFENSIVE_DEBUFF = 9
    COWARDLY = 10
    SLEEPING = 11
    STUNNED = 12
    UNKNOWN = 13