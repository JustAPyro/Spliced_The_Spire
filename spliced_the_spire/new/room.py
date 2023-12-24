from abstractions import *
from abc import ABC, abstractmethod
from enemies import *
from math import floor

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

class BigFish(AbstractEventChoices):
    def __init__(self, actor):
        super(BigFish, self).__init__(actor=actor)
        self.actor = actor

    def Banana(self):
        healthGain = floor(self.actor.health / 3)
        self.actor.heal(healthGain)

    def Donut(self):
        self.actor.increase_max_health(5)

    def Box(self):
        pass
        # relic, curse

