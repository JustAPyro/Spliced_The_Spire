import random
from typing import Callable


class Condition:
    def __init__(self, ability):
        self.ability = ability


class PercentChance(Condition):
    def __init__(self, percent: int, ability: Callable):
        super().__init__(ability)
        self.percent = percent


class AbilityGenerator:
    def __init__(self):
        self.samples = []
        self.weights = []
        self.total_percent = 0

    def condition(self, condition: Condition):
        if type(condition) == PercentChance:
            condition: PercentChance
            self.samples.append(condition.ability)
            self.weights.append(condition.percent)

    def finalize(self):

        while True:
            yield random.choices(self.samples, self.weights, k=1)


def hi():
    return True


def bye():
    return False

