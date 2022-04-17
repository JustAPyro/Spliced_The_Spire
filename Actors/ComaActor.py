# A TERRIBLE AI that is in a coma and does NOTHING EVER
from Actors.AbstractActor import Actor


from Actors import AbstractActor


class ComaAI(AbstractActor):
    def __init__(self, cards):
        AbstractActor.__init__(self, cards, 72)
        
        
    def take_turn(self):
        print("Coma AI is in a coma and does nothing.")
