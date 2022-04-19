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
            ["75%", "3X"]: self.__bite()  # 75% chance of biting, cannot use 3 times in a row
        })

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

    def conditionalChanceBasedAction(self, actionMap):

        # Start by assuming a probability of 100
        totalProbability = 100
        bannedMethods = []

        # This adjusts total probability and adds anything that shouldn't occur to bannedMethods
        for based, method in actionMap.items():
            percent, times = based  # unpack the percent and times

            if times.replace("X", "") == "":
                continue  # This was an empty conditional, so skip it

            # Get the history for x number of turns
            history = self.actionHistory[-times.replace("X", ""):]

            # If we did this method last turn AND we've done the same method for each of the last turn
            if history[-1] == method and len(set(history)) <= 1:

                # Reduce the total probability because we will not be allowing this to occur
                totalProbability -= percent.replace("%")
                bannedMethods.append(method)

