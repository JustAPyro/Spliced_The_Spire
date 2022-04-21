import math

from src.Monsters import Cultist
from random import randint

health = dict()


def generateSamples(function, quantity):
    samples = dict()
    for i in range(quantity):
        out = function()
        if out not in samples.keys():
            samples[out] = 0
        samples[out] += 1
    return samples

