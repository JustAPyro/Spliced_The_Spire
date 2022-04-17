from random import randint


class RandomChance:
    def __init__(self, *args):
        self.chances = args

        if sum(args) != 100:
            raise DoesNotAddTo100

        self.total = 0

    def chance(self, useThisChance):

        # error
        if useThisChance not in self.chances:
            raise ChanceNotDeclared

        if useThisChance + self.total >= randint(1, 100):
            return True

        self.total += useThisChance
        return False


class ChanceNotDeclared(Exception):
    """
    Tried to use a .chance not declared
    """
    pass


class DoesNotAddTo100(Exception):
    """
    chances do not add to 100
    """
    pass
