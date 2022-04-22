from src.Monsters.AbstractMonster import AbstractMonster
from Effects import Strength, Block
from functools import partial


class JawWorm(AbstractMonster):
    def __init__(self, ascension=1, act=1):
        AbstractMonster.__init__(self,
                                 name="Jaw Worm",
                                 max_health={
                                     1: (40, 44),  # A1- Health is 40-44
                                     7: (42, 46)  # A7+ Health is 42-46
                                 },
                                 ascension=ascension,
                                 act=act
                                 )

    def onStart(self):
        #  Add strength and block
        self.addEffect(Block(self, 0))
        self.addEffect(Strength(self, 0))

        # If this is Act 3 we start with a bellow
        if self.act == 3:
            self._bellow()

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
        if self.turn == 0 and self.act == 1:
            return self.useAction(self._chomp)

        # Otherwise, we follow this logic
        ability = self.conditionalChanceBasedAction({
            ("45%", "2X"): partial(self._bellow),
            ("30%", "3X"): partial(self._thrash),
            ("25%", "2X"): partial(self._chomp)
        })

        # Then use the super-class API to use it, returning the results
        return self.useAction(ability)

    def _chomp(self):
        """ Attack player

        Specification:
        A < 2: Does 11 Damage
        Else: Does 12 Damage
        """

        ability = self.ascensionBasedAction({
            1: partial(self.getPlayer().takeDamage, 11),
            2: partial(self.getPlayer().takeDamage, 12)
        })

        ability()  # Use ability
        return self._chomp  # And return

    def _thrash(self):
        """ Attacks player and gains block

        Specification:
        Deal 7 damage, gain 5 block.
        """

        # deals 7 damage to player
        self.getPlayer().takeDamage(7)

        # this monster gains 5 block
        self.gainBlock(5)

        return self._thrash

    def _bellow(self):
        """ Monster gains strength and block.

        Specifications:
        <A1> +3 Strength, +6 Block
        <A2> +4 Strength, +6 block
        <A17> +5 Strength, +9 block

        """

        strengthAction = self.ascensionBasedAction({
            +1: partial(self.modifyEffect, "Strength", 3),
            +2: partial(self.modifyEffect, "Strength", 4),
            17: partial(self.modifyEffect, "Strength", 5)
        })

        blockAction = self.ascensionBasedAction({
            +1: partial(self.modifyEffect, "Block", 6),
            17: partial(self.modifyEffect, "Block", 9)
        })

        # Actually use the abilities and return
        strengthAction()
        blockAction()
        return self._bellow
