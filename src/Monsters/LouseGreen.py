from random import randint

from src.Monsters.AbstractMonster import AbstractMonster


class LouseGreen(AbstractMonster):
    def __init__(self, ascension=1):
        AbstractMonster.__init__(self,
                                 name="Louse",
                                 max_health={
                                     1: (11, 17),
                                     7: (12, 18)
                                 },
                                 ascension=ascension,
                                 act=1)

        action = self.ascensionBasedAction({
            +1: self.modifyEffect("Curl Up", randint(3, 7)),
            +7: self.modifyEffect("Curl Up", randint(4, 8)),
            17: self.modifyEffect("Curl Up", randint(9, 12))
        })
        action()

        # Randomly picks damage at beginning of fight
        self.damage = randint(5, 7)

    def take_turn(self):

        if self.ascension < 17:
            action = self.conditionalChanceBasedAction({
                ["25%", "3X"]: self.__spitWeb(),
                ["75%", "3X"]: self.__bite()
            })
            action()
            return

        if self.ascension >= 17:
            action = self.conditionalChanceBasedAction({
                ["25%", "2X"]: self.__spitWeb(),
                ["75%", "3X"]: self.__bite()
            })
            action()
            return

        raise Exception()

    # - - - - - Monster Abilities - - - - - #

    def __bite(self):
        action = self.ascensionBasedAction({
            1: lambda: self.getPlayer().takeDamage(self.damage),
            2: lambda: self.getPlayer().takeDamage(self.damage + 1)
        })
        action()

    def __spitWeb(self):
        self.getPlayer().modifyEffect("Weak", 2)
