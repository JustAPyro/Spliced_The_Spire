
from abc import ABC, abstractmethod


class AbstractGame(ABC):
    def __init__(self, ascension, wonLastGame, actor):
        self.ascension = ascension
        self.wonLastGame = wonLastGame
        self.actor = actor

        # generate map
        # TODO: self.map = SOMEONE ELSE DO THIS HELP
        self.floor = 0

    def startGame(self):
        # Neow Event
        #
        pass

    def chooseNextRoom(self):
        pass
