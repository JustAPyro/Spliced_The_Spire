from src.Effects.AbstractEffect import AbstractEffect


class Strength(AbstractEffect):
    def __init__(self, strength=0):
        AbstractEffect.__init__(self,
                                name="Strength",
                                effectType="Buff",
                                decreaseOverTime=False)
        self.strength = strength

    def modifyDamageDealt(self, dmg):
        return dmg + self.strength



