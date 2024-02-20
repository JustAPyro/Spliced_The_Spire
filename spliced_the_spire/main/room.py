from abstractions import *
from abc import ABC, abstractmethod
from enemies import *
from relics import *
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

class Neow(AbstractEventChoices):
    def __init__(self, actor, hasWonLastGame: bool):
        super(Neow, self).__init__(actor=actor)
        self.hasWonLastGame = hasWonLastGame
        self.actor = actor

    def simulateRoom(self):
        if self.hasWonLastGame:
            pass

        # loser
        else:
            # choose max hp +, or next 3 enemies have 1 hp relic

            self.actor.select_option(options=[self._increaseMaxHealth,
                                              self._enemyHealthDownRelic],
                                     event=EventNames.NEOW)

        self._roomFinished()

    def _increaseMaxHealth(self):
        healthGain = 8
        if self.actor.color.RED:
            self.actor.increase_max_health(healthGain)

        elif not self.actor.color.GREEN:
            healthGain -= 1
            self.actor.increase_max_health(healthGain)

        else:
            healthGain -= 2
            self.actor.increase_max_health(healthGain)

    def _enemyHealthDownRelic(self):
        self.actor.relics.append(NeowsLament())


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

    def simulateRoom(self):
        pass