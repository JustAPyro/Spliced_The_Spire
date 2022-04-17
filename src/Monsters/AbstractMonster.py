from abc import ABC, abstractmethod
from src.Effects import Strength

class AbstractMonster(ABC):

    def __init__(self, name, max_health, ascension, act=1):
        self.name = name
        self.max_health = max_health
        self.current_health = max_health
        self.turn = 0

        self.block = 0
        self.strength = Strength()

        # Some defaults that need to be set before using
        self.ascension = ascension
        self.act = act
        self.actor = None
        self.actionHistory = []

    def deal_damage(self, damage):
        adjustedDamage = self.strength.modifyDamageDealt(damage)
        self.getPlayer().takeDamage(adjustedDamage)

    def take_damage(self, dmg):
        self.current_health -= dmg

    def setPlayer(self, actor):
        self.actor = actor

    def getPlayer(self):
        return self.actor

    def gainBlock(self, block):
        self.block += block

    def gainStrength(self, strength):
        self.strength.strength += strength

    @abstractmethod
    def take_turn(self):
        pass
