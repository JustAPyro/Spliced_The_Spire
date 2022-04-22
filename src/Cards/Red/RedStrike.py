from src.Cards.AbstractCard import AbstractCard


class RedStrike(AbstractCard):
    def __init__(self):
        AbstractCard.__init__(self,
                              name="Strike",
                              energy_cost=1)

    def useCard(self, target):
        pass
