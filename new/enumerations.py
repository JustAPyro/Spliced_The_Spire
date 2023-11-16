from enum import Enum


class SelectEvent(Enum):
    DRAW = 1
    EXHAUST = 2
    PLACE_ON_DRAWPILE = 3
    COPY = 4


class CardPiles(Enum):
    DRAW = 1
    HAND = 2
    DISCARD = 3
    EXHAUST = 4


class CardType(Enum):
    ATTACK = 1
    SKILL = 2
    POWER = 3
    STATUS = 4
    CURSE = 5