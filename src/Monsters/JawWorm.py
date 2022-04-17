from src.Monsters.AbstractMonster import AbstractMonster
from src.Utility.HomeUtility import RandomChance
from random import randint


class JawWorm(AbstractMonster):
    def __init__(self, health=None, ascension=0):
        AbstractMonster.__init__(self,
                                 name="Jaw Worm",
                                 max_health=health,
                                 ascension=ascension,
                                 act=1
                                 )

        # no specific health
        if health is None:
            if self.ascension < 7:
                self.max_health = randint(40, 44)
            else:
                self.max_health = randint(42, 46)

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


        """

        # T1: starting move is always the same unless in act 3
        if self.act is not 3 and self.turn is 1:
            self.chomp()
            return

        monsterHasFinished = False

        # keep looping until monster has completed an action
        while not monsterHasFinished:

            actionChoice = RandomChance(30, 45, 25)

            # 45% change
            if actionChoice.chance(45):

                # can not use bellow twice in a row
                if len(self.actionHistory) > 0 and self.actionHistory[-1] == "bellow":
                    continue

                self.bellow()
                self.actionHistory.append("bellow")

                # monster is done with turn
                monsterHasFinished = True

            # 30% chance
            elif actionChoice.chance(30):

                # Can not thrash three times in a row
                if len(self.actionHistory) > 0 and self.actionHistory[-2] == self.actionHistory[-1] == "thrash":
                    continue

                self.thrash()
                self.actionHistory.append("thrash")

                # monster is done with turn
                monsterHasFinished = True

            # 25% chance
            elif actionChoice.chance(25):

                # cannot use chomp twice in a row
                if len(self.actionHistory) > 0 and self.actionHistory[-1] == "chomp":
                    continue

                self.chomp()
                self.actionHistory.append("chomp")

                # monster is done with turn
                monsterHasFinished = True

    def chomp(self):
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

    def thrash(self):
        """ Attacks player and gains block

        Specification:
        Deal 7 damage, gain 5 block.
        """

        # deals 7 damage to player
        self.getPlayer().takeDamage(7)

        # this monster gains 5 block
        self.gainBlock(5)

    def bellow(self):
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
