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

        # Red Louse starts with a Curl Up power
        action = self.ascensionBasedAction({
            1: lambda: self.modifyEffect("Curl Up", randint(3, 7)),
            7: lambda: self.modifyEffect("Curl Up", randint(4, 8)),
            17: lambda: self.modifyEffect("Curl Up", randint(9, 12))
        })
        action()

        # TODO: between 5 and 7? 6?
        self.damage = randint(5, 7)

    def take_turn(self):
        action = self.conditionalChanceBasedAction({
            ["25%", "3X"]: self.__grow(),  # 25% chance of growing, cannot use 3 times in a row
            ["75%", "3X"]: self.__bite()   # 75% chance of biting, cannot use 3 times in a row
        })
        action()

    # - - - - - Monster Abilities - - - - -

    def __bite(self):
        action = self.ascensionBasedAction({
            1: lambda: self.getPlayer().takeDamage(self.damage),
            2: lambda: self.getPlayer().takeDamage(self.damage + 1)
        })
        action()

    def __grow(self):
        action = self.ascensionBasedAction({
            +1: lambda: self.modifyEffect("Strength", 3),
            17: lambda: self.modifyEffect("Strength", 4)
        })
        action()


