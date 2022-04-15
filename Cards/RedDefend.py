from AbstractCard import AbstractCard


class RedDefend(AbstractCard):
    def __init__(self):
        super().__init__(
            name="Defend",
            energy_cost=1
        )

    def useCard(self, target):
        target.block += 5
