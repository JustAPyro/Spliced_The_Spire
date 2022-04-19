from src.Effects.AbstractEffect import AbstractEffect


# CLEAN 4/17
class Ritual(AbstractEffect):
    def __init__(self, target, quantity):       # Constructor
        AbstractEffect.__init__(self, target,   # Call super-constructor
                                name="Ritual",
                                effectType="Buff",
                                decreaseOverTime=False,
                                quantity=quantity)

    def onTurnEnd(self):
        # Increase strength by quantity (number of stacks)
        self.target.modifyEffect("Strength", self.quantity)
