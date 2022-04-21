from src.Monsters.AbstractMonster import AbstractMonster
from functools import partial

class JawWorm(AbstractMonster):
    def __init__(self, health=None, ascension=0):
        AbstractMonster.__init__(self,
                                 name="Jaw Worm",
                                 max_health={
                                     1: (40, 44),  # A1- Health is 40-44
                                     7: (42, 46)  # A7+ Health is 42-46
                                 },
                                 ascension=ascension,
                                 act=1
                                 )

        # special for act 3
        if self.act == 3:
            self.bellow()

    def take_turn(self):
        """ Defines how the monster takes its

        Specifications:
        T1: Chomp
        T2:
            45%: Bellow
            30%: Thrash
            25%: Chomp
            -> Cannot Bellow 2x in a row
            -> Cannot Thrash 3x in a row
            -> Cannot Chomp 2x in a row

        If in Act 3:
            Start with buffs from bellow, and no guarantee for chomp first turn

        """
        # If it's our first turn, and we're in act one, we chomp
        if self.turn == 1 and self.act == 1:
            self._chomp()

        # Otherwise, we follow this logic
        self.conditionalChanceBasedAction({
            ["45%", "2X"]: partial(self._bellow),
            ["30%", "3X"]: partial(self._thrash),
            ["25%", "2X"]: partial(self._chomp)
        })


    def _chomp(self):
        """ Attack player

        Specification:
        A < 2: Does 11 Damage
        Else: Does 12 Damage
        """

        if self.ascension < 2:

            # deals 11 damage to player
            self.getPlayer().takeDamage(11)

        # A2 +
        else:

            # deals 12 damage to player
            self.getPlayer().takeDamage(12)

    def _thrash(self):
        """ Attacks player and gains block

        Specification:
        Deal 7 damage, gain 5 block.
        """

        # deals 7 damage to player
        self.getPlayer().takeDamage(7)

        # this monster gains 5 block
        self.gainBlock(5)

    def _bellow(self):
        """ Monster gains strength and block

        Specifications:
        <A2: Gain 4 strength, 6 block
        <A17: Gain 4 Stength, 6 block
        else: Gain 5 strength, 9 block

        """

        if self.ascension < 2:
            self.gainStrength(3)
            self.gainBlock(6)

        # A2 +
        elif self.ascension < 17:
            self.gainStrength(4)
            self.gainBlock(6)

        # A17 +
        else:
            self.gainStrength(5)
            self.gainBlock(9)
