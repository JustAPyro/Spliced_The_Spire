from spliced_the_spire.main.cards import *
from spliced_the_spire.main.relics import BurningBlood

class STSClass():
    pass


class Ironclad(STSClass):
    health = 80

    #start_relic = BurningBlood()

    start_cards = [
        RedStrike(),
        RedStrike(),
        RedStrike(),
        RedStrike(),
        RedStrike(),
        RedDefend(),
        RedDefend(),
        RedDefend(),
        RedDefend(),
        Bash(),
    ]

    cards = (
        RedStrike(),
        RedStrike(),
        RedStrike(),
        RedStrike(),
        RedStrike(),
        RedDefend(),
        RedDefend(),
        RedDefend(),
        RedDefend(),
        Bash(),
    )
