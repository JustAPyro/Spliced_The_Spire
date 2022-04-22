from src.Effects.AbstractEffect import AbstractEffect


class Block(AbstractEffect):
    def __init__(self, target, quantity):
        AbstractEffect.__init__(self, target,
                                name="Block",
                                effectType="Buff",
                                decreaseOverTime=False,
                                quantity=quantity)
