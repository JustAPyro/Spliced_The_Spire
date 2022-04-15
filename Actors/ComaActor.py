# A TERRIBLE AI that is in a coma and does NOTHING EVER
from Actors.AbstractActor import Actor


class ComaAI(Actor):
    def __init__(self, cards):
        Actor.__init__(self, cards, 72)
        
        
    def take_turn(self):
        print("Coma AI is in a coma and does nothing.")
