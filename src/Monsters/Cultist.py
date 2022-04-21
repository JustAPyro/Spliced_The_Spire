from src.Monsters.AbstractMonster import AbstractMonster
from functools import partial


# Clean & Tested 4/21/22
class Cultist(AbstractMonster):
    def __init__(self, ascension=1):
        AbstractMonster.__init__(self,
                                 name="Cultist",
                                 max_health=({
                                     1: (48, 54),  # A1- Health is 48-54
                                     7: (50, 56)  # A7+ Health is 50-56
                                 }),
                                 ascension=ascension,
                                 act=1)

    def take_turn(self):
        # If it's our first turn
        if self.turn == 0:
            # Use incantation and end turn
            self._incantation()
            return self._incantation

        # After that we dark strike every turn
        self._darkStrike()
        return self._darkStrike

    # Tested
    def _incantation(self):
        # Ritual gain is based on ascension
        action = self.ascensionBasedAction({
            +1: partial(self.modifyEffect, "Ritual", 3),  # A1- Gain 3 Ritual
            +2: partial(self.modifyEffect, "Ritual", 4),  # A2+ Gain 4 Ritual
            17: partial(self.modifyEffect, "Ritual", 5)  # A17+ Gain 5 Ritual
        })
        action()

        # Increment our turn then return
        self.turn += 1
        return self._incantation

    # Tested
    def _darkStrike(self):
        # Dark strike always does 6 damage
        self.getPlayer().takeDamage(6)

        # End turns by returning dark strike
        self.turn += 1
        return self._darkStrike
