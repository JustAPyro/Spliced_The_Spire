from abc import ABC, abstractmethod
from src.Effects import Strength, Ritual

from random import randint


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
    ascensionBounds = max_health.keys().sort()

    # We need to have defined behavior for ascension 1+ at least
    if ascensionBounds[0] is not 1:
        raise Exception

    # starting from the second ascension, and increasing
    for i in range(1, len(ascensionBounds)):

        # Check if this ascension is lower than the next ascension
        if ascension < ascensionBounds[i]:
            # If so, generate and return health based on the previous range
            low, high = max_health[ascensionBounds[i - 1]]
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
            self.max_health = calculateHealth(max_health, ascension)

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
        self.strength = Strength()

        # Some defaults that need to be set before using

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

    def modify(self, effect, quantity):
        """ Used to modify (+/-) the quantity of an effect

        :param effect: The effect you want modified
        :param quantity: The quantity (positive or negative) you want changed
        :return: None
        """
        self.effects[effect].modify(quantity)

    @abstractmethod
    def take_turn(self):
        pass
