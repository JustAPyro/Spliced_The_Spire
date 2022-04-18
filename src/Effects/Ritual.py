from src.Effects.AbstractEffect import AbstractEffect


# CLEAN 4/17
class Ritual(AbstractEffect):
    def __init__(self, target, quantity):
        AbstractEffect.__init__(self, target,
                                name="Ritual",
                                effectType="Buff",
                                decreaseOverTime=False,
                                quantity=quantity)

    def onTurnEnd(self):
        self.target.modifyEffect("Strength", self.quantity)
