from src.Monsters.AbstractMonster import AbstractMonster


class Cultist(AbstractMonster):
    def __init__(self, ascension=1):
        AbstractMonster.__init__(self,
                                 name="Cultist",
                                 max_health=({
                                     1: (48, 54),   # A1- Health is 48-54
                                     7: (50, 56)    # A7+ Health is 50-56
                                 }),
                                 ascension=ascension,
                                 act=1)

    def take_turn(self):

        # If it's our first turn
        if self.turn() is 0:
            # Use incantation and end turn
            self.incantation()
            return

        # After that we dark strike every turn
        self.darkStrike()

    def incantation(self):
        # Ritual gain is based on ascension
        self.ascensionBased({
            1: lambda: self.modifyEffect("Ritual", 3),  # A1- Gain 3 Ritual
            2: lambda: self.modifyEffect("Ritual", 4),  # A2+ Gain 4 Ritual
            17: lambda: self.modifyEffect("Ritual", 5)  # A17+ Gain 5 Ritual
        })

    def darkStrike(self):
        # Dark strike always does 6 damage
        self.getPlayer().takeDamage(6)
