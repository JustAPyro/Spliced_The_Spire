class StrikeRed(Card):
    def __init__(self):
        # Declare the basic information by calling superclass constructor
        super().__init__(
            name="Strike",
            energy_cost=1)

    def useCard(self, target_actor):
        target_actor.take_damage(6)
