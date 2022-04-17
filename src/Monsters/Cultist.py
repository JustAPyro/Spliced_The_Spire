from src.Monsters.AbstractMonster import AbstractMonster


class Cultist(AbstractMonster):
    def __init__(self, ascension):
        AbstractMonster.__init__(self,
                                 name="Cultist",
                                 max_health=None,
                                 ascension=ascension,
                                 act=1)



    def take_turn(self):
        pass