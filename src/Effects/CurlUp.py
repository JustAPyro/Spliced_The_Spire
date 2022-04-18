from src.Effects.AbstractEffect import *


class CurlUp(AbstractEffect):
    def __init__(self, target, quantity):
        AbstractEffect.__init__(self, target,
                                name="Curl Up",
                                effectType="Buff",
                                decreaseOverTime=False,
                                quantity=quantity)

    def afterDamageReceived(self):
        # When damage is received, increase block by quantity and then remove this buff
        self.target.modifyEffect("Block", self.quantity)
        self.quantity = 0
