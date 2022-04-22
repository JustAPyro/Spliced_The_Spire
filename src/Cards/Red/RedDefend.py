from src.Cards.AbstractCard import AbstractCard


class RedDefend(AbstractCard):
    def __init__(self):
        AbstractCard.__init__(self,
                              name="Defend",
                              energy_cost=1)

    def useCard(self, target):
        pass
