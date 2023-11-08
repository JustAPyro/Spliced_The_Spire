from new.cards import *
from new.relics import Burning_Blood

class STSClass():
    pass


class Ironclad(STSClass):
    health = 80

    start_relic = Burning_Blood()

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
