from src.Monsters.AbstractMonster import AbstractMonster
from random import randint


class RedLouse(AbstractMonster):
    def __init__(self, ascension=1):
        AbstractMonster.__init__(self,
                                 name="Louse",
                                 max_health={
                                     1: (10, 15),
                                     7: (11, 16)
                                 },
                                 ascension=ascension,
                                 act=1)

        self.ascensionBased({
            1: lambda: self.modifyEffect("Curl Up", randint(3, 7)),
            7: lambda: self.modifyEffect("Curl Up", randint(4, 8)),
            17: lambda: self.modifyEffect("Curl Up", randint(9, 12))
        })

        # TODO: between 5 and 7? 6?
        self.damage = randint(5, 7)

    def take_turn(self):
        pass

    def __bite(self):
        pass

    def __grow(self):
        pass