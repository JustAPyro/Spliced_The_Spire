from abc import ABC, abstractmethod
from src.Effects import Strength, Ritual

from random import randint
from functools import partial

# Calculates health by ascension
def calculateHealth(max_health, ascension):
    """ Calculates health based on the dict and provided ascension level
    ex.
    { 1:(0, 100), 5:(100, 200) } -> Health(0, 100), A5+ Health(100, 200)
    Note: The first entry must be A1, otherwise Exception will be raised.

    :param max_health: A dict in the format ascension: (low, high)
    :param ascension: The ascension you want to generate health for
    :return: A random health in the range of provided ascension
    """

    # Start with a sorted list of the ascension bounds
    ascensionBounds = list(max_health.keys())
    ascensionBounds.sort()

    # We need to have defined behavior for ascension 1+ at least
    if ascensionBounds[0] != 1:
        raise Exception

    # starting from the second ascension, and increasing
    for i in range(0, len(ascensionBounds)):

        # Check if this ascension is lower than the next ascension
        if ascension <= ascensionBounds[i]:
            # If so, generate and return health based on the previous range
            low, high = max_health[ascensionBounds[i]]
            return randint(low, high)

        # If it's not lower than the highest bound, then we know to use the last range
        low, high = max_health[ascensionBounds[-1]]
        return randint(low, high)


class AbstractMonster(ABC):

    def __init__(self, name, max_health, ascension, act=1):
        self.name = name
        self.ascension = ascension
        self.act = act

        # Assign the health
        if type(max_health) is dict:
            # If a dict was provided calculate health based on that
            self.max_health = self._ascensionBasedRandomValue(max_health)

        else:
            # Otherwise, just use the provided value
            max_health = max_health

        # Set all buffs to zero and initialize them
        self.effects = {
            "Ritual": Ritual(self, 0)  # Default start with 0 Ritual
        }

        # Since this monster was just created, set current health to max
        self.current_health = max_health
        self.turn = 0
        self.block = 0
        self.strength = Strength(self, 0)

        # Some defaults that need to be set before using

        self.actor = None
        self.actionHistory = []

    def deal_damage(self, damage):
        adjustedDamage = self.strength.modifyDamageDealt(damage)
        self.getPlayer().takeDamage(adjustedDamage)

    def useAction(self, ability):
        """ API for having a monster use an ability.
        By calling this method the super-class will automatically handle things like:
        - Incrementing turn
        - Returning the correct method
        :param ability: The ability you want to use
        :return: The ability used
        """

        ability()       # Start by using the ability
        self.turn += 1  # Increment turn

        # Then, if it's a partial, get and return only the function
        if type(ability) is partial:
            return partial.func

        # Otherwise, just return the as is
        return ability


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

    def modifyEffect(self, effect, quantity):
        """ Used to modify (+/-) the quantity of an effect

        :param effect: The effect you want modified
        :param quantity: The quantity (positive or negative) you want changed
        :return: None
        """
        self.effects[effect].quantity += quantity

    def getEffect(self, effect):
        return self.effects[effect].quantity

    def conditionalChanceBasedAction(self, actionMap):

        # Start by assuming a probability of 100
        totalProbability = 100
        bannedMethods = []
        probabilities = []

        # This adjusts total probability and adds anything that shouldn't occur to bannedMethods
        for based, method in actionMap.items():
            percent, times = based  # unpack the percent and times

            # Save the probabilities to our list
            probabilities.append(based)

            if times.replace("X", "") == "":
                continue  # This was an empty conditional, so skip it

            # Get the history for x number of turns
            history = self.actionHistory[-times.replace("X", ""):]

            # If we did this method last turn AND we've done the same method for each of the last turn
            if history[-1] == method and len(set(history)) <= 1:
                # Reduce the total probability because we will not be allowing this to occur
                totalProbability -= percent.replace("%", "")
                bannedMethods.append(method)

        # Sort the keys based on likelihood (lowest first)
        probabilities.sort(key=lambda x: int(x[0].replace("", "")))

        # Start with probability 0
        prob = 0

        # Generate a random number
        roll = randint(0, totalProbability)

        # Then for each key/probability
        for probability in probabilities:
            prob += int(probability[0].replace("%", ""))
            if roll <= prob:
                return actionMap[probability]

        raise Exception

    def ascensionBasedAction(self, actionDict):

        # Sort keys
        ascensionBounds = list(actionDict.keys())
        ascensionBounds.sort()

        # We need to have defined behavior for ascension 1+ at least
        if ascensionBounds[0] != 1:
            raise Exception

        # starting from the second ascension, and increasing
        for i in range(0, len(ascensionBounds)-1):

            # Check if this ascension is lower than the next ascension
            if self.ascension < ascensionBounds[i+1]:

                # If so, generate and return health based on the previous range
                return actionDict[ascensionBounds[i]]

        # If it's not lower than the highest bound, then we know to use the last range
        return actionDict[ascensionBounds[-1]]

    def _ascensionBasedRandomValue(self, valueDict):
        """
        Use this to get a random value based on ascension
        Returns a random value in a range based on ascension
        :param valueDict: {1: (5, 10)} -> For ascension 1+ random(5, 10)
        :return: A random number in the provided range based on the ascension of this monster
        """
        # Create a lambda function and insert it in to a generator map for each trny
        generatorDict = dict()
        for key in valueDict:
            low, high = valueDict[key]
            generatorDict[key] = partial(randint, low, high)

        # Get an ascension based action
        generator = self.ascensionBasedAction(generatorDict)

        # Return the results of the generator
        return generator()

    def ascensionBasedValue(self, valueDict):
        pass

    @abstractmethod
    def take_turn(self):
        pass
