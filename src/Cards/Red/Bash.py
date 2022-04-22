from src.Cards.AbstractCard import AbstractCard


class Bash(AbstractCard):
    def __init__(self):
        AbstractCard.__init__(self,
                              name="Bash",
                              energy_cost=2)

    def useCard(self, target):
        pass
