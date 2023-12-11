from enum import Enum


class SelectEvent(Enum):
    DRAW = 1
    EXHAUST = 2
    PLACE_ON_DRAWPILE = 3
    COPY = 4,
    RECOVER_FROM_EXHAUST = 5


class CardPiles(Enum):
    DRAW = 1
    HAND = 2
    DISCARD = 3
    EXHAUST = 4

    @classmethod
    def all(cls):
        return CardPiles.DRAW, CardPiles.HAND, CardPiles.DISCARD, CardPiles.EXHAUST


class CardType(Enum):
    ATTACK = 1
    SKILL = 2
    POWER = 3
    STATUS = 4
    CURSE = 5

    @staticmethod
    def all():
        return CardType.ATTACK, CardType.SKILL, CardType.POWER, CardType.STATUS, CardType.CURSE
