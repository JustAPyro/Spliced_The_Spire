from Cards.AbstractCard import AbstractCard


class RedStrike(AbstractCard):
    def __init__(self):
        # Declare the basic information by calling superclass constructor
        super().__init__(
            name="Strike",
            energy_cost=1)

    def useCard(self, target):
        target.take_damage(6)
