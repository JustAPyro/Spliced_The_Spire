
from abc import ABC, abstractmethod


class AbstractRoom(ABC):
    def __init__(self, actor, ascension, floor, act):
        pass
        # shop: cards to buy
        # elite: enemies to fight
        # boss: enemies to fight
        # combat: enemies to fight
        # unknown: random options happen
        # neow: choices made


class Shop(AbstractRoom, ABC):
    def __init__(self, actor, ascension, floor, act):
        # shop items
        super().__init__(actor, ascension, floor, act)


class AbstractUnknown(AbstractRoom, ABC):
    def __init__(self, actor, ascension, floor, act):
        super().__init__(actor, ascension, floor, act)


class BigFish(AbstractUnknown, AbstractRoom, ABC):

    def __init__(self, actor, ascension, floor, act):
        super().__init__(actor, ascension, floor, act)




