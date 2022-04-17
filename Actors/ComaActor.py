# A TERRIBLE AI that is in a coma and does NOTHING EVER
from Actors.AbstractActor import AbstractActor


class ComaAI(AbstractActor):
    def __init__(self, cards):
        AbstractActor.__init__(self, cards, 51)


    def take_turn(self):  # noqa
        print("Coma AI is in a coma and does nothing.")
