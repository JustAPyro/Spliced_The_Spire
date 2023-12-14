
from abc import ABC, abstractmethod


class AbstractGame(ABC):
    def __init__(self, ascension, wonLastGame, actor):
        self.ascension = ascension
        self.wonLastGame = wonLastGame
        self.actor = actor

        self.floor = 0

    def startGame(self):
        # starting choices
        pass

