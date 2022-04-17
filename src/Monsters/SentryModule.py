# Sentry monster
from src.Monsters.AbstractMonsterModule import AbstractMonster
from random import randint


class Sentry(AbstractMonster):

    # Define a sentry by calling abstract base class constructor
    def __init__(self, health=None, attack_first=True, ascension=0, act=1):

        AbstractMonster.__init__(self,
                                 name="Sentry",
                                 max_health=health,
                                 ascension=ascension,
                                 act=act)

        # no explicit health given
        if health is None:

            # ascension less than 8
            if self.ascension < 8:

                # higher health range
                health = randint(38, 42)

            # higher health range because of ascension
            else:

                # health
                health = randint(39, 45)



        # If we're attacking first start counter at 0
        self.ability_counter = 0
        if (not attack_first):  # Otherwise start it at 1
            self.ability_counter = 1

    def take_turn(self):

        # Alternate, if ability counter is even beam, otherwise bolt
        if self.ability_counter % 2 == 0:
            self.beam()
        else:
            self.bolt()
        self.ability_counter += 1  # Increment the ability counter now

    # Beam ability
    # Asc 3+ does 10 damage
    # Asc <= 3 does 9 damage
    def beam(self):
        print("> Sentry casts beam:", end=' ')
        if self.ascension <= 3:
            self.actor.takeDamage(9)
        else:
            self.actor.takeDamage(10)

    # Bolt ability
    # Asc 18+ shuffles 3 Dazed into discard pile
    # Asc <= 18 shuffles 2 Dazed into discard pile
    def bolt(self):
        print("> Sentry casts bolt: player shuffles 2 Dazed into discard pile")
        self.actor.shuffle_in("Dazed", self.actor.discard_pile)
