from src.Effects.AbstractEffect import AbstractEffect


class Strength(AbstractEffect):
    def __init__(self, target, quantity):
        AbstractEffect.__init__(self, target,
                                name="Strength",
                                effectType="Buff",
                                decreaseOverTime=False,
                                quantity=quantity)

    def modifyDamageDealt(self, dmg):
        return dmg + self.quantity



