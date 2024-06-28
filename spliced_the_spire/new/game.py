from enumerations import *
from abstractions import *
from actors import *
from classes import *
from room import *
from enemies import *


player = AbstractActor(clas=Ironclad, environment=None, color=Color.RED)

AbstractCombat(actor=player, enemies=[RedLouse], isElite=False, isBoss=False)


