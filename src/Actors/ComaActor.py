# A TERRIBLE AI that is in a coma and does NOTHING EVER
from src.Actors.AbstractActor import AbstractActor


class ComaAI(AbstractActor):
    def __init__(self, cards, max_health):
        AbstractActor.__init__(self, cards, max_health)

    def take_turn(self):  # noqa
        print("Coma AI is at", self.current_health, "in a coma and does nothing.")
