from abc import ABC


class AbstractEffect(ABC):
    def __init__(self, target, name, effectType, decreaseOverTime, quantity):

        # Set the standard instance variables passed in
        self.target = target
        self.name = name
        self.effectType = effectType
        self.decreaseOverTime = decreaseOverTime
        self.quantity = quantity

    def onTurnStart(self):
        pass

    def onTurnEnd(self):
        pass

    def afterDamageReceived(self):
        pass

    def modifyDamageDealt(self, dmg):
        pass

    def modifyDamageTaken(self, dmg):
        pass

    def modifyDefense(self):
        pass

    def modifyQuantity(self, quantity):
        self.quantity += quantity
