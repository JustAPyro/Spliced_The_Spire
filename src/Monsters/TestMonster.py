from src.Monsters.AbstractMonster import AbstractMonster


class TestMonster(AbstractMonster):
    def __init__(self, health):
        AbstractMonster.__init__(self,
                                 name="Test Monster",
                                 max_health=health,
                                 ascension=1)

    def take_turn(self):
        pass
