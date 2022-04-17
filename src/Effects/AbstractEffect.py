from abc import ABC


class AbstractEffect(ABC):
    def __init__(self, name, effectType, decreaseOverTime):
        self.name = name
        self.effectType = effectType
        self.decreaseOverTime = decreaseOverTime

    def onTurnStart(self):
        pass

    def onTurnEnd(self):
        pass

    def modifyDamageDealt(self, dmg):
        pass

    def modifyDamageTaken(self, dmg):
        pass

    def modifyDefense(self):
        pass
