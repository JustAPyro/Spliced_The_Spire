from abc import ABC, abstractmethod


class AbstractMonster(ABC):

    def __init__(self, name, max_health):
        self.name = name
        self.max_health = max_health
        self.current_health = max_health
        self.turn = 0
        self.block = 0

        # Some defaults that need to be set before using
        self.ascention = 0
        self.actor = None

    def take_damage(self, dmg):
        self.current_health -= dmg

    @abstractmethod
    def take_turn(self):
        pass
