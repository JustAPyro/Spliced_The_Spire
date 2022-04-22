from src.Actors.AbstractActor import AbstractActor


class RandomActor(AbstractActor):
    def __init__(self, cards, max_health):
        AbstractActor.__init__(self, cards, max_health, name="Random Actor")

    def take_turn(self):  # noqa
        print("Coma AI is at", self.current_health, "in a coma and does nothing.")
