from abstractions import *
from abc import ABC, abstractmethod
from enemies import *

# combat rooms


class CultistRoom(AbstractCombat):
    def __init__(self):

        super(CultistRoom, self).__init__(enemies=[Cultist()],
                                          isElite=False,
                                          isBoss=False,
                                          floor=self.floor)


class JawWormRoom(AbstractCombat):
    pass


class LouseRoom(AbstractCombat):
    pass


class SmallSlimeRoom(AbstractCombat):
    pass


# unknown rooms



