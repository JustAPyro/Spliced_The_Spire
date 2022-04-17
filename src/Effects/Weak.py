import math

from src.Effects.AbstractEffect import AbstractEffect


class Weak(AbstractEffect):
    def __init__(self):
        AbstractEffect.__init__(self,
                                name="Weakness",
                                effectType="De-buff",
                                decreaseOverTime=True)
        turnsWeakened = 0

    def modifyDamageDealt(self, dmg):
        return math.floor(dmg * 0.25)
