
from enumerations import *
from abstractions import *
from actors import *
from classes import *
from room import *
from enemies import *

player = AbstractActor(clas=Ironclad)

myFight = AbstractCombat(actor=player, enemies=[RedLouse()], isElite=False, isBoss=False)
print(myFight.enemies[0].implemented_hooks)
myFight.beginRoom()

myFight.printRoom()

myFight.playerTurn()

myFight.printRoom()
