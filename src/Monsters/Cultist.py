from src.Monsters.AbstractMonster import AbstractMonster


class Cultist(AbstractMonster):
    def __init__(self, ascension):
        AbstractMonster.__init__(self,
                                 name="Cultist",
                                 max_health=({
                                     1: (48, 54),  # A1- Health is 48-54
                                     7: (50, 56)   # A7+ Health is 50-56
                                 }),
                                 ascension=ascension,
                                 act=1)

    def take_turn(self):
        pass

    def incantation(self):
        pass

    def darkStrike(self):
        pass
